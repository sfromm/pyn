#!/usr/bin/python

'''
check for changes (using snmpv3) to running configuration.
if there is a change, send email.
'''

from email_helper import send_email
from snmp_helper import snmp_extract, snmp_get_oid
from optparse import OptionParser

# HARD CODE IT!  :P
SENDER = 'nobody@localhost'
OIDS = {'sysUpTime' : '1.3.6.1.2.1.1.3.0',
        'runningLastChanged' : '1.3.6.1.4.1.9.9.43.1.1.1.0',
        'runningLastSaved'   : '1.3.6.1.4.1.9.9.43.1.1.2.0',
        'startupLastChanged' : '1.3.6.1.4.1.9.9.43.1.1.3.0' }

def get_host_oid(snmpdev, snmpuser, oid):
    output = snmp_extract( snmp_get_oid_v3(snmpdev, snmpuser, oid=oid) )

def main(args):
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
        snmp_user = ( options.username, optoins.authkey, options.encryptkey )
        data[arg] = {}
        for name, oid in OIDS.iteritems():
            data[arg][name] = check_host( (host, port), snmp_user, OIDS['sysUpTime'] )

    for host in data:
        if data[host]['runningLastChanged'] > data[host]['runningLastSaved']:
            subject = '%s running configuration changed' % host
            message = subject + " at %s" % data[host]['runningLastChanged']
            if options.debug:
                print message
            else:
                send_email(options.email, subject, message, SENDER)

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt, e:
        print >> sys.stderr, "Exiting on user request.\n"
        sys.exit(1)
