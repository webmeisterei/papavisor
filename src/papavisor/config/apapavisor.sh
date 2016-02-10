##
# Config file for apapvisor - apapvisor searches for supervisord cfg files.
# Gets sources by the apapavisor script.
#
##

# These lines get passed to "ls -1 <line> | xargs"
SEARCH_CFG=(
    '/home/zope/*/parts/supervisor/supervisord.conf'
)

# Each line here is correspondending to the ls line above.
# it gets called like: "echo <file_path> | sed -e <sed_regex_from_below>"
# and should return the projects name.
NAME_SED=(
    's#.*zope/\(.*\)/parts/.*#\1#i'
)

PAPAVISOR="$(which papavisor)"
