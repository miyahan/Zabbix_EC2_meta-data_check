#!/bin/env python

import argparse
import sys

from zabbix.api import ZabbixAPI


ZABBIX_SERVER = 'http://localhost/zabbix'
ZABBIX_USER = 'username'
ZABBIX_PASSWORD = 'password'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete host from Zabbix server')
    parser.add_argument('-n', '--hostname', required=True, help='Zabbix hostname')
    args = parser.parse_args()

    zapi = ZabbixAPI(url=ZABBIX_SERVER, user=ZABBIX_USER, password=ZABBIX_PASSWORD)

    """Get hostid by hostname"""
    result = zapi.do_request(
        'host.get',
        {
            'filter': {'host': [args.hostname]},
            'output': ['name', 'hostid']
        }
    )

    if not result['result']:
        sys.exit('hostname not found')

    """Delete host from Zabbix server"""
    hostid = result['result'][0]['hostid']
    result = zapi.do_request('host.delete', [hostid])
    print(result)
