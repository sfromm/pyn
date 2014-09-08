#!/usr/bin/python

from snmp_helper import snmp_extract, snmp_get_oid
from optparse import OptionParser
import sys

# HARD CODE IT!  :P
OIDS = {'sysUpTime' : '1.3.6.1.2.1.1.3.0',
        'runningLastChanged' : '1.3.6.1.4.1.9.9.43.1.1.1.0',
        'runningLastSaved'   : '1.3.6.1.4.1.9.9.43.1.1.2.0',
        'startupLastChanged' : '1.3.6.1.4.1.9.9.43.1.1.3.0' }

def main(args):
    parser = OptionParser()
    parser.add_option('-c', '--community', default='public', help='community string')
    parser.add_option('-D', '--debug', action='store_true', help='be verbose')
    options, args = parser.parse_args()

    data = {}
    for arg in args:
        host, port = arg.split(':')
        device = (host, options.community, port)
        data[arg] = {}
        for name, oid in OIDS.iteritems():
            data[arg][name] = snmp_extract(snmp_get_oid(device, oid=oid))
    for host in data:

# From the mib:
# If the value of ccmHistoryRunningLastChanged is greater than
# ccmHistoryRunningLastSaved, the configuration has been
# changed but not saved.

        if options.debug:
            print data[host]

        if data[host]['runningLastChanged'] > data[host]['runningLastSaved']:
            print "%s config modified (%s), but not saved (%s)" % (
                host, data[host]['runningLastChanged'], data[host]['startupLastChanged']
            )


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
