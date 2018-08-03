#!/usr/bin/env python

from subprocess import call
import math, json, sys, os, argparse, subprocess

print "**************************************************"
print "**          Tested on Ubuntu 14.04 LTS          **"
print "**             Mesos version 0.26.0              **"
print "**************************************************"

parser = argparse.ArgumentParser(prog="donkey-proc")
parser.add_argument('--domain', '-d',
	dest= 'domain' , help='Domain of the server', required=True)
parser.add_argument('--config', '-c',
	dest= 'config' , help='Config (.json) file', required=True)

args = parser.parse_args()

with open(str(os.getcwd())  + "/" + str(args.config)) as cfgfile:
	conf = json.load(cfgfile)

	print "config file : ", json.dumps(conf, indent=2)
	mctr = len(conf['MASTERS'])
	sctr = len(conf['SLAVES'])

	zkaddr = conf['MASTERS'][0]['ipaddr'] + ':2181'
	for i in xrange(mctr - 1):
		zkaddr = zkaddr + ',' + conf['MASTERS'][i + 1]['ipaddr'] + ':2181'
	quorum = int(math.ceil(mctr / 2.0))

	for i in xrange(mctr):
		hostname = str(conf['MASTERS'][i]['name']) + '.' + str(args.domain)
		print "Accessing " + hostname + " over ssh..."
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install software-properties-common'])
		subprocess.call(['ssh','root@' + hostname, 'echo "Installing Dependency: Oracle Java 8"'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-add-repository ppa:webupd8team/java'])

		subprocess.call(['ssh','root@' + hostname, 'echo "Adding Mesosphere Repository"'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF'])
		# subprocess.call(['ssh','root@' + hostname, 'export DISTRO=$(lsb_release -is | tr "[:upper:]" "[:lower:]")'])
		# subprocess.call(['ssh','root@' + hostname, 'export CODENAME=$(lsb_release -cs)'])

		subprocess.call(['ssh','root@' + hostname, 'DISTRO=$(lsb_release -is | tr "[:upper:]" "[:lower:]"); CODENAME=$(lsb_release -cs); echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y update'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install oracle-java8-installer'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install mesos=0.26*'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install marathon=0.13.0*'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install chronos=2.4.0*'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install zookeeper=3.4.5*'])

		subprocess.call(['ssh','root@' + hostname, 'echo "Configuring Zookeeper"'])
		subprocess.call(['ssh','root@' + hostname, 'echo "zk://' + zkaddr + '/mesos" | sudo tee /etc/mesos/zk'])
		subprocess.call(['ssh','root@' + hostname, 'echo ' + conf['MASTERS'][i]['id'] + ' | sudo tee /etc/zookeeper/conf/myid'])
		subprocess.call(['ssh','root@' + hostname, '[ -f /etc/zookeeper/conf/zoo.cfg.ori ] && echo "Original zoo.cfg is already stored" || sudo cp /etc/zookeeper/conf/zoo.cfg /etc/zookeeper/conf/zoo.cfg.ori'])
		subprocess.call(['ssh','root@' + hostname, 'echo "Overwrite zoo.cfg"'])
		subprocess.call(['ssh','root@' + hostname, 'echo "tickTime=2000" | sudo tee /etc/zookeeper/conf/zoo.cfg'])
		subprocess.call(['ssh','root@' + hostname, 'echo "initLimit=10" | sudo tee -a /etc/zookeeper/conf/zoo.cfg'])
		subprocess.call(['ssh','root@' + hostname, 'echo "syncLimit=5" | sudo tee -a /etc/zookeeper/conf/zoo.cfg'])
		subprocess.call(['ssh','root@' + hostname, 'echo "dataDir=/var/lib/zookeeper" | sudo tee -a /etc/zookeeper/conf/zoo.cfg'])
		subprocess.call(['ssh','root@' + hostname, 'echo "clientPort=2181" | sudo tee -a /etc/zookeeper/conf/zoo.cfg'])
		subprocess.call(['ssh','root@' + hostname, 'echo "The Original zoo.cfg is kept safe at zoo.cfg.ori"'])
		subprocess.call(['ssh','root@' + hostname, 'echo "Setting Quorum"'])
		subprocess.call(['ssh','root@' + hostname, 'echo ' + str(quorum) + ' | sudo tee /etc/mesos-master/quorum'])
		subprocess.call(['ssh','root@' + hostname, 'echo ' + conf['MASTERS'][i]['ipaddr'] + ' | sudo tee /etc/mesos-master/ip'])
		subprocess.call(['ssh','root@' + hostname, 'sudo cp /etc/mesos-master/ip /etc/mesos-master/hostname'])
		subprocess.call(['ssh','root@' + hostname, 'echo "Configuring Marathon"'])
		subprocess.call(['ssh','root@' + hostname, 'sudo mkdir -p /etc/marathon/conf'])
		subprocess.call(['ssh','root@' + hostname, 'sudo cp /etc/mesos-master/hostname /etc/marathon/conf'])
		subprocess.call(['ssh','root@' + hostname, 'sudo cp /etc/mesos/zk /etc/marathon/conf/master'])
		subprocess.call(['ssh','root@' + hostname, 'echo "zk://' + zkaddr + '/marathon" | sudo tee /etc/marathon/conf/zk'])

		for j in xrange(mctr):
			ret = subprocess.call(['ssh','root@' + hostname,
				'echo "server.' + conf['MASTERS'][j]['id'] + '=' + conf['MASTERS'][j]['ipaddr'] + ':2888:3888" | sudo tee -a /etc/zookeeper/conf/zoo.cfg'])

	for i in xrange(mctr):
		hostname = str(conf['MASTERS'][i]['name']) + '.' + str(args.domain)
		print "Start Mesos-Master Service on " + hostname + "..."

		subprocess.call(['ssh','root@' + hostname,'sudo stop mesos-slave'])
		subprocess.call(['ssh','root@' + hostname,'echo manual | sudo tee /etc/init/mesos-slave.override'])
		subprocess.call(['ssh','root@' + hostname,'sudo restart zookeeper'])
		subprocess.call(['ssh','root@' + hostname,'sudo start mesos-master'])
		subprocess.call(['ssh','root@' + hostname,'sudo start marathon'])

	for i in xrange(sctr):
		hostname = str(conf['SLAVES'][i]['name']) + '.' + str(args.domain)
		print "Accessing " + hostname + " over ssh..."
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install software-properties-common'])
		subprocess.call(['ssh','root@' + hostname, 'echo "Installing Dependency: Oracle Java 8"'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-add-repository ppa:webupd8team/java'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y update'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install oracle-java8-installer'])

		subprocess.call(['ssh','root@' + hostname, 'echo "Adding Mesosphere Repository"'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF'])
		# subprocess.call(['ssh','root@' + hostname, 'DISTRO=$(lsb_release -is | tr "[:upper:]" "[:lower:]")'])
		# subprocess.call(['ssh','root@' + hostname, 'CODENAME=$(lsb_release -cs)'])
		subprocess.call(['ssh','root@' + hostname, 'DISTRO=$(lsb_release -is | tr "[:upper:]" "[:lower:]"); CODENAME=$(lsb_release -cs); echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y update'])
		subprocess.call(['ssh','root@' + hostname, 'echo "Installing Mesos"'])
		subprocess.call(['ssh','root@' + hostname, 'sudo apt-get -y install mesos=0.26*'])
		subprocess.call(['ssh','root@' + hostname, 'echo "Configuring Zookeeper"'])
		subprocess.call(['ssh','root@' + hostname, 'echo "zk://' + zkaddr + '/mesos" | sudo tee /etc/mesos/zk'])

	for i in xrange(sctr):
		hostname = str(conf['SLAVES'][i]['name']) + '.' + str(args.domain)
		print "Start Mesos-Slave Service on " + hostname + "..."

		subprocess.call(['ssh','root@' + hostname, 'sudo stop zookeeper'])
		subprocess.call(['ssh','root@' + hostname, 'echo manual | sudo tee /etc/init/zookeeper.override'])
		subprocess.call(['ssh','root@' + hostname, 'echo manual | sudo tee /etc/init/mesos-master.override'])
		subprocess.call(['ssh','root@' + hostname, 'sudo stop mesos-master'])
		subprocess.call(['ssh','root@' + hostname, 'echo ' + conf['SLAVES'][i]['ipaddr'] + ' | sudo tee /etc/mesos-slave/ip'])
		subprocess.call(['ssh','root@' + hostname, 'sudo cp /etc/mesos-slave/ip /etc/mesos-slave/hostname'])
		subprocess.call(['ssh','root@' + hostname, 'sudo start mesos-slave'])
