#!/usr/bin/env python

from subprocess import call
import sys, os, argparse, subprocess

parser = argparse.ArgumentParser(prog="donkey-proc")
parser.add_argument('--domain', '-d',
	dest= 'domain' , help='Domain of the server', required=True)
parser.add_argument('--hostname', '-n',
	dest= 'hostname' , help='Hostname of the server', required=True)
parser.add_argument('--start', '-s',
	dest= 'start_index' , help='Prefix number of slave index start', required=True)
parser.add_argument('--finish', '-f',
	dest= 'stop_index' , help='Prefix number of slave index stop', required=True)

args = parser.parse_args()

for i in xrange(int(args.start_index), int(args.stop_index) + 1):
    print "Accessing " + str(args.hostname) + str(i) + '.' + str(args.domain) + "over ssh ..."

    if "mesos-slave" in str(args.hostname):
        ret = subprocess.call(['scp',str(os.getcwd()) + '/install-slave.sh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain) + ':/root'])

        ret = subprocess.call(['ssh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain),
            'bash install-slave.sh'])

        ret = subprocess.call(['ssh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain),
            'rm install-slave.sh'])

    if "mesos-master" in str(args.hostname):
        ret = subprocess.call(['scp',str(os.getcwd()) + '/install-master.sh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain) + ':/root'])

        ret = subprocess.call(['ssh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain),
            'bash install-master.sh'])

        ret = subprocess.call(['ssh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain),
            'rm install-master.sh'])

	print "Finish processing "+ str(args.hostname) + str(i) + '.' + str(args.domain) + " over ssh ..."
