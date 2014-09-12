#!/usr/bin/python

'''
poll device every 5 minutes for one hour
create two graphs: one of octets and the other of unicast pkts
'''

from snmp_helper import *
from optparse import OptionParser
import datetime
import time
import sys
import pprint
import pygal

# HARD CODE IT!  :P
OIDS = {'ifHCInOctets'     : '1.3.6.1.2.1.31.1.1.1.6',
        'ifHCOutOctets'    : '1.3.6.1.2.1.31.1.1.1.10',
        'ifHCInUcastPkts'  : '1.3.6.1.2.1.31.1.1.1.7',
        'ifHCOutUcastPkts' : '1.3.6.1.2.1.31.1.1.1.11'}

def get_host_oid(snmpdev, oid):
    '''
    args: (host, comstr, port) tuple
    oid: SNMP OID
    '''
    return snmp_extract(snmp_get_oid(snmpdev, oid=oid))

def get_host_oid_v3(snmpdev, snmpuser, oid):
    '''
    args:
    snmpdev: (host, port) tuple
    snmpuser: (snmpv3_username, snmpv3_authkey, snmpv3_encrypt_key) tuple
    oid: SNMP OID
    '''
    return snmp_extract( snmp_get_oid_v3(snmpdev, snmpuser, oid=oid) )

def line_graph(title, xlabels, datapoints, path):
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = xlabels
    for name, data in datapoints.iteritems():
        line_chart.add(name, data)
    line_chart.render_to_file(path)

def main(args):
    ''' main '''
    parser = OptionParser()
    parser.add_option('-I', '--index', default=5, help='index')
    parser.add_option('-i', '--interval', type='int', default=300, help='interval')
    parser.add_option('-c', '--count', default=12, help='count')
    parser.add_option('-C', '--community', default='public', help='community string')
    parser.add_option('--host', help='host:port')
    parser.add_option('-D', '--debug', action='store_true', help='be verbose')
    options, args = parser.parse_args()

    data = {}
    xlabels = []
    last = {}
    for n in OIDS.keys():
        last[n] = None

    if options.debug:
        print "querying %s, interval=%s, count=%s" % (
            options.host, options.interval, options.count
        )
    for i in range(0, int(options.count)):
        host, port = options.host.split(':')
        xlabels.append( datetime.datetime.now().minute )
        for name, oid in OIDS.iteritems():
            if name not in data:
                data[name] = []
            val = get_host_oid( (host, options.community, port), 
                                "%s.%s" % (OIDS[name], options.index))
            val = int(val)
            if options.debug:
                print "%s=%s" % (name, val)
            if last[name] is None:
                last[name] = val
            else:
                data[name].append(int(val) - last[name])
                last[name] = val
        if options.debug:
            print datetime.datetime.now()
            pprint.pprint(data)
        time.sleep(options.interval)

    line_graph('Input/Output Bandwidth', xlabels,
               {'Input'  : data['ifHCInOctets'],
                'Output' : data['ifHCOutOctets']}, 'bits.svg')
    line_graph('Input/Output Packets', xlabels,
               {'Input'  : data['ifHCInUcastPkts'],
                'Output' : data['ifHCOutUcastPkts']}, 'pkts.svg')



if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
