#!/bin/env python

import argparse
import sys

from zabbix.api import ZabbixAPI


ZABBIX_SERVER = 'http://localhost/zabbix'
ZABBIX_USER = 'username'
ZABBIX_PASSWORD = 'password'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Register instance-id to Zabbix host-macro')
    parser.add_argument('-n', '--hostname', required=True, help='Zabbix hostname')
    parser.add_argument('-i', '--instanceid', required=True, help='EC2 instance-id')
    args = parser.parse_args()

    if not args.hostname:
        sys.exit('ERROR: hostname is empty')
    if not args.instanceid:
        sys.exit('ERROR: instanceid is empty')
    if args.instanceid == 'unknown':
        sys.exit('unknown')
    if args.instanceid[0:2] != 'i-':
        sys.exit('ERROR: invalid instanceid')

    zapi = ZabbixAPI(url=ZABBIX_SERVER, user=ZABBIX_USER, password=ZABBIX_PASSWORD)

    """Get hostid by hostname"""
    result = zapi.do_request(
        'host.get',
        {
            'filter': {
                'host': [args.hostname]
            },
            'output': ['name', 'hostid']
        }
    )

    if not result['result']:
        sys.exit('not found' % args.hostname)

    """Update host macro"""
    hostid = result['result'][0]['hostid']
    result = zapi.do_request(
        'host.update',
        {
            'hostid': hostid,
            'macros': [
                {
                    'macro': '{$EC2_INSTANCEID}',
                    'value': args.instanceid,
                }
            ]
        }
    )
    print(result['result'])
