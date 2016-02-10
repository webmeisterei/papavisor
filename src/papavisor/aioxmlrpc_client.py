#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML-RPC Client with asyncio.
This module adapt the ``xmlrpc.client`` module of the standard library to
work with asyncio.

Original (BSD) source: https://github.com/mardiros/aioxmlrpc/blob/master/aioxmlrpc/client.py
"""
from __future__ import print_function

import asyncio
import base64
import logging
import socket
from xmlrpc import client as xmlrpc

import aiohttp

__ALL__ = ['ServerProxy', 'Fault', 'ProtocolError']

# you don't have to import xmlrpc.client from your code
Fault = xmlrpc.Fault
ProtocolError = xmlrpc.ProtocolError

log = logging.getLogger(__name__)


class _Method:
    # some magic to bind an XML-RPC method to an RPC server.
    # supports "nested" methods (e.g. examples.getStateName)
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, "%s.%s" % (self.__name, name))

    @asyncio.coroutine
    def __call__(self, *args):
        ret = yield from self.__send(self.__name, args)
        return ret


class AioTransport(xmlrpc.Transport):
    """
    ``xmlrpc.Transport`` subclass for asyncio support
    """

    user_agent = 'python/aioxmlrpc'

    def __init__(self, use_https, *, username=None, password=None,
                 uri=None, use_datetime=False,
                 use_builtin_types=False, loop=None):
        super().__init__(use_datetime, use_builtin_types)
        self._loop = loop or asyncio.get_event_loop()

        self.use_https = use_https
        self._username = username
        self._password = password
        self._loop = loop
        if not uri:
            self._connector = aiohttp.TCPConnector(loop=self._loop)
        elif uri.startswith('unix://'):
            self._connector = aiohttp.UnixConnector(
                path=uri[7:], loop=self._loop
            )
        else:
            self._connector = aiohttp.TCPConnector(loop=self._loop)

    @asyncio.coroutine
    def request(self, host, handler, request_body, verbose):
        """
        Send the XML-RPC request, return the response.
        This method is a coroutine.
        """
        headers = {'User-Agent': self.user_agent,
                   #Proxy-Connection': 'Keep-Alive',
                   #'Content-Range': 'bytes oxy1.0/-1',
                   'Accept': 'text/xml',
                   'Content-Type': 'text/xml' }

        # basic auth
        if self._username is not None and self._password is not None:
            unencoded = "%s:%s" % (self._username, self._password)
            encoded = base64.encodestring(
                bytes(unencoded, encoding='utf-8')
            )
            headers["Authorization"] = "Basic %s" % (
                str(encoded.decode()).replace('\n', '')
            )

        url = self._build_url(host, handler)
        response = None
        try:
            response = yield from aiohttp.request(
                'POST', url, headers=headers, data=request_body,
                connector=self._connector, loop=self._loop)
            body = yield from response.read()
            if response.status != 200:
                raise ProtocolError(url, response.status,
                                    body, response.headers)
        except ProtocolError:
            raise
        except aiohttp.errors.ClientOSError as e:
            raise ProtocolError(
                errcode=500,
                errmsg=e.strerror,
                headers=headers,
                url=url
            )

        return self.parse_response(body)

    def parse_response(self, body):
        """
        Parse the xmlrpc response.
        """
        p, u = self.getparser()
        p.feed(body)
        p.close()
        return u.close()

    def close(self):
        super(AioTransport, self).close()

        self._connector.close()

    def _build_url(self, host, handler):
        """
        Build a url for our request based on the host, handler and use_http
        property
        """
        scheme = 'https' if self.use_https else 'http'
        return '%s://%s%s' % (scheme, host, handler)


class ServerProxy(xmlrpc.ServerProxy):
    """
    ``xmlrpc.ServerProxy`` subclass for asyncio support
    """

    def __init__(self, uri, *, username=None, password=None,
                 transport=None, encoding=None, verbose=False,
                 allow_none=False, use_datetime=False,use_builtin_types=False,
                 loop=None):
        self._loop = loop or asyncio.get_event_loop()
        if not transport:
            transport = AioTransport(
                uri.startswith('https://'),
                uri=uri,
                username=username,
                password=password,
                loop=self._loop)

        if uri.startswith('unix://'):
            uri = 'http://localhost'
        super().__init__(uri, transport, encoding, verbose, allow_none,
                         use_datetime, use_builtin_types)

    @asyncio.coroutine
    def __request(self, methodname, params):
        # call a method on the remote server
        request = xmlrpc.dumps(params, methodname, encoding=self.__encoding,
                               allow_none=self.__allow_none).encode(self.__encoding)

        response = yield from self.__transport.request(
            self.__host,
            self.__handler,
            request,
            verbose=self.__verbose
            )

        if len(response) == 1:
            response = response[0]

        return response

    def __getattr__(self, name):
        if name == 'close':
            return self.__close
        elif name == 'transport':
            return self.__transport
        else:
            return _Method(self.__request, name)
