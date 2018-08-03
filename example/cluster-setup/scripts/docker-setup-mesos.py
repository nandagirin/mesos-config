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

	ret = subprocess.call(['ssh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain), 
		"echo 'docker,mesos' | sudo tee /etc/mesos-slave/containerizers"])

	ret = subprocess.call(['ssh','root@' + str(args.hostname) + str(i) + '.' + str(args.domain), 
		"restart mesos-slave"])

	print "Finish processing "+ str(args.hostname) + str(i) + '.' + str(args.domain) + " over ssh ..."

