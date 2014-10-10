#!/usr/bin/python

'''
Use eAPI to enumerate interfaces and display (In|Out)Octets
'''

from jsonrpclib import Server
from optparse import OptionParser
import sys
import json

def main(args):
    ''' main '''
    parser = OptionParser()
    parser.add_option('-u', '--username', default='eapi', help='username')
    parser.add_option('-p', '--password', default='', help='password')
    parser.add_option('-P', '--port', default='8543', help='port')
    parser.add_option('-D', '--debug', action='store_true', help='debug')
    options, args = parser.parse_args()

    for switch in args:
        url = "https://{0}:{1}@{2}:{3}/command-api".format(
            options.username, options.password, switch, options.port
        )
        request = Server(url)
        response = request.runCmds(1, ["show interfaces"] )
        if options.debug:
            print json.dumps(response, indent=4, sort_keys=True)
        interfaces = sorted(response[0]['interfaces'].keys())
        print "Switch {0} interfaces:".format(switch)
        print "{:20} {:<20} {:<20}".format("Interface", "inOctets", "outOctets")
        for inf in interfaces:
            data = response[0]['interfaces'][inf]
            if 'interfaceCounters' in data:
                print "{:20} {:<20} {:<20}".format(
                    inf, data['interfaceCounters']['inOctets'], data['interfaceCounters']['outOctets']
                )
        print


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
