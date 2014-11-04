#!/usr/bin/python

''' print interface stats '''

from onepk_helper import NetworkDevice
from onep.interfaces import NetworkInterface, InterfaceFilter
import yaml
import sys

def main(args):
    ''' main '''
    rtrs = yaml.load(file(args[0]).read())
    for rtr in rtrs:
        ndev = NetworkDevice(**rtr)
        ndev.connect()

        print "Connection established to: %s" % ndev.net_element.properties.sys_name
        InterfaceTypes = NetworkInterface.InterfaceTypes
        filter = InterfaceFilter(None, InterfaceTypes.ONEP_IF_TYPE_ETHERNET)
        ndev_if = ndev.net_element.get_interface_list(filter)
        for inf in ndev_if:
            print "%s interface stats:" % inf.name
            print inf.get_statistics()

        ndev.disconnect()

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
