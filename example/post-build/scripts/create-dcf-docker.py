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
	print "Accessing mesos-slave" + str(i) + ".smdonkey.com over ssh ..."
	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D'])
	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >> /etc/apt/sources.list.d/docker.list'])
	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'apt-get update -y'])
	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'apt-get purge -y lxc-docker'])
	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'apt-cache policy docker-engine'])
	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'apt-get install -y linux-image-extra-$(uname -r)'])
	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'sudo apt-get install -y docker-engine'])

	ret = subprocess.call(['ssh','root@' + str(hostname) + str(i) + '.' + str(domain), 'docker run hello-world'])
	print "Finish installing docker on mesos-slave" + str(i) + ".smdonkey.com over ssh ..."
