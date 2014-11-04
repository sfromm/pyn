#!/usr/bin/python

from onepk_helper import NetworkDevice
import yaml
import sys

def main(args):
    ''' main '''
    rtrs = yaml.load(file(args[0]).read())
    for rtr in rtrs:
        ndev = NetworkDevice(**rtr)
        ndev.connect()

        print "Connection established to: %s" % ndev.net_element.properties.sys_name
        print ndev.net_element.properties.product_id
        print ndev.net_element.properties.SerialNo

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
