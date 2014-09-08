#!/usr/bin/python

from snmp_helper import snmp_extract, snmp_get_oid
from optparse import OptionParser
import sys

# HARD CODE IT!  :P
OIDS = { 'sysName' : '1.3.6.1.2.1.1.5.0' ,
         'sysDescr' : '1.3.6.1.2.1.1.1.0' }

def main(args):
    parser = OptionParser()
    parser.add_option('-c', '--community', default='public', help='community string')
    options, args = parser.parse_args()

    for arg in args:
        host, port = arg.split(':')
        device = (host, options.community, port)
        for name, oid in OIDS.iteritems():
            print snmp_extract(snmp_get_oid(device, oid=oid))

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
