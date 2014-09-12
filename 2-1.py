#!/usr/bin/python

'''
check for changes (using snmpv3) to running configuration.
if there is a change, send email.
'''

from email_helper import send_mail
from snmp_helper import *
from optparse import OptionParser
import sys
import pprint

# HARD CODE IT!  :P
SENDER = 'nobody@localhost'
OIDS = {'sysUpTime' : '1.3.6.1.2.1.1.3.0',
        'runningLastChanged' : '1.3.6.1.4.1.9.9.43.1.1.1.0',
        'runningLastSaved'   : '1.3.6.1.4.1.9.9.43.1.1.2.0',
        'startupLastChanged' : '1.3.6.1.4.1.9.9.43.1.1.3.0' }

def get_host_oid_v3(snmpdev, snmpuser, oid):
    '''
    args:
    snmpdev: (host, port) tuple
    snmpuser: (snmpv3_username, snmpv3_authkey, snmpv3_encrypt_key) tuple
    oid: SNMP OID
    '''
    return snmp_extract( snmp_get_oid_v3(snmpdev, snmpuser, oid=oid) )

def main(args):
    ''' main '''
    parser = OptionParser()
    parser.add_option('-u', '--username', default='pysnmp', help='snmpv3 username')
    parser.add_option('-a', '--authkey', help='snmpv3 authkey')
    parser.add_option('-e', '--encryptkey', help='snmpv3 encryptkey')
    parser.add_option('--email', default='nobody@localhost', help='email recipient')
    parser.add_option('-D', '--debug', action='store_true', help='be verbose')
    options, args = parser.parse_args()

    data = {}
    for arg in args:
        host, port = arg.split(':')
        snmp_user = ( options.username, options.authkey, options.encryptkey )
        data[arg] = {}
        if options.debug:
            print "querying %s" % arg
        for name, oid in OIDS.iteritems():
            data[arg][name] = get_host_oid( (host, port), snmp_user, OIDS[name])

    if options.debug:
        pprint.pprint(data)

    for host in data:
        if data[host]['startupLastChanged'] == 0:
            continue
        elif data[host]['runningLastChanged'] > data[host]['startupLastChanged']:
            subject = '%s running configuration changed' % host
            message = subject + " at %s" % data[host]['runningLastChanged']
            if options.debug:
                print message
            else:
                # bleh
                send_mail(options.email, subject, message, SENDER)

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
