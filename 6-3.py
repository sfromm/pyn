#!/usr/bin/python

''' use vty service to get output '''

from onepk_helper import NetworkDevice
from onep.vty import VtyService
import yaml
import sys

CMDS = ['terminal length 0', 'show version']

def main(args):
    ''' main '''
    rtrs = yaml.load(file(args[0]).read())
    for rtr in rtrs:
        ndev = NetworkDevice(**rtr)
        ndev.connect()

        print "Connection established to: %s" % ndev.net_element.properties.sys_name
        vty_svc = VtyService(ndev.net_element)
        vty_svc.open()
        for cmd in CMDS:
            out = vty_svc.write(cmd)
            print out

        ndev.disconnect()

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
