#!/bin/env python

import argparse
import sys

import boto3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get EC2 instance status from AWS')
    parser.add_argument('-r', '--region', required=True, help='AWS region name')
    parser.add_argument('-a', '--accesskey', required=True, help='AWS access key')
    parser.add_argument('-s', '--secretkey', required=True, help='AWS secret key')
    parser.add_argument('-i', '--instanceid', required=True, help='EC2 instance-id')
    args = parser.parse_args()

    if not args.region:
        sys.exit('ERROR: region is empty')
    if not args.accesskey:
        sys.exit('ERROR: accesskey is empty')
    if not args.secretkey:
        sys.exit('ERROR: secretkey is empty')
    if not args.instanceid:
        sys.exit('ERROR: instanceid is empty')
    if args.instanceid == 'unknown':
        sys.exit('unknown')
    if args.instanceid[0:2] != 'i-':
        sys.exit('ERROR: invalid instanceid')

    ec2 = boto3.session.Session(
        aws_access_key_id=args.accesskey,
        aws_secret_access_key=args.secretkey).client('ec2', args.region)

    instances = ec2.describe_instances(
        InstanceIds=[args.instanceid]
    )

    state = None
    for reservations in instances['Reservations']:
        for instance in reservations['Instances']:
            state = instance['State']['Name']

    if not state:
        sys.exit('not found')

    print(state)
