papavisor
=========

A control script for supervisor's - the Papa (german Dad) of supervisors.

With papavisor you can:

- Get the status of all supervisors one a machine (you can configure remote supervisor though).
- Start/stop/restart grouped supervisor `programs` with priorities and `startsecs` in between.
- Talk to multiple supervisors in parallel (by using asyncio).
- apapavisor finds supervisord.cfg files himself - no need to configure each instance.


Requirements
============

- Unix like System
- Python >3.4.0

Install
=======

papavisor is available over `pypi <https://pypi.python.org/pypi/papavisor>`_::

    $ pip3 install papavisor

It will copy 2 config files to ``/etc/papavisor``

- **00_default.json** - The default config file for all supervisors
- **01_template.json** - A Template with comments for a project.
- **apapavisor.sh** - The config file for ``Auto Papavisor``


Configuration
=============

All configuration files live in ``/etc/papavisor``, papavisor reads all **.json** files sorted and merges
them into one big configuration OrderedDict.

**papavisor** files:

- **00_default.json** - Contains the defaults for each project, they will get copied and then overwritten by the per project values.
- **01_template.json** - An template for "manual" project witch overwrites the defaults above.

**apapavisor** - The **Auto papavisor** reads **apapavisor.sh** only.



Usage
=====

When you install this package you get two excecutables:

- **papavisor**     -   The supervisord control script.
- **apapavisor**    -   A wrapper witch searches for `supervisord.conf` files and passes them to papavisor, its the `Auto papavisor` as you need nearly no configuration for that.

General usage::

    $ (a)papavisor [project-or-all] [action] [group-or-program]

The default is::

    $ (a)papavisor all status all

For example, to restart all zope instances::

    $ apapavisor all restart zopes

To restart all python stuff on project ploneconf::

    $ apapavisor plonec restart python

All actions::

    $ apapvaisor <project-or-all> status <group-or-program>
    $ apapavisor <project-or-all> start <group-or-program>
    $ apapavisor <project-or-all> stop <group-or-program>
    $ apapavisor <project-or-all> restart <group>


Authors
=======
- Rene´ Jochum <rene@webmeisterei.com>
- Idea from `@frisi <https://github.com/frisi>`_.


License
=======

papavisor is licensed under the MIT license.


Contribute
==========

- Issue Tracker: https://github.com/webmeisterei/papavisor/issues
- Source Code: https://github.com/webmeisterei/papavisor


Support
=======

If you are having issues, please let us know.
