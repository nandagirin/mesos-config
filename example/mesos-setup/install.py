#!/usr/bin/env python

from subprocess import call
import math, json, sys, os, argparse, subprocess

print "**************************************************"
print "**          Tested on Ubuntu 14.04 LTS          **"
print "**             Mesos version 1.1.0              **"
print "**************************************************"

parser = argparse.ArgumentParser(prog="donkey-proc")
parser.add_argument('--domain', '-d',
	dest= 'domain' , help='Domain of the server', required=True)
parser.add_argument('--config', '-c',
	dest= 'config' , help='Config (.json) file', required=True)

args = parser.parse_args()

with open(str(os.getcwd())  + "/" + str(args.config)) as cfgfile:
    conf = json.load(cfgfile)

    mctr = len(conf['MASTERS'])
    sctr = len(conf['SLAVES'])

    zkaddr = conf['MASTERS'][0]['ipaddr'] + ':2181'
    for i in xrange(mctr - 1):
        zkaddr = zkaddr + ',' + conf['MASTERS'][i + 1]['ipaddr'] + ':2181'
    quorum = int(math.ceil(mctr / 2.0))

    for i in xrange(mctr):
        hostname = str(conf['MASTERS'][i]['name']) + '.' + str(args.domain)
        print "Accessing " + hostname + " over ssh..."

		ret = subprocess.call(['ssh','root@' + hostname,
            'echo "Installing Dependency: Oracle Java 8"',
            'sudo apt-add-repository ppa:webupd8team/java',
            'sudo apt-get -y update',
            'sudo apt-get -y install oracle-java8-installer',
            'echo "Adding Mesosphere Repository"',
			'sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF',
			'DISTRO=$(lsb_release -is | tr "[:upper:]" "[:lower:]")',
			'CODENAME=$(lsb_release -cs)',
			'echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list',
			'sudo apt-get -y update',
			'echo "Installing Mesosphere"',
			'sudo apt-get -y install mesosphere',
			'echo "Configuring Zookeeper"',
			'echo "zk://' + zkaddr + '/mesos" | sudo tee /etc/mesos/zk',
			'echo ' + conf['MASTERS'][i]['id'] + ' | sudo tee /etc/zookeeper/conf/myid',
			'[ -f /etc/zookeeper/conf/zoo.cfg.ori ] && echo "Original zoo.cfg is already stored" || sudo cp /etc/zookeeper/conf/zoo.cfg /etc/zookeeper/conf/zoo.cfg.ori',
			'echo "Overwrite zoo.cfg"',
			'echo "tickTime=2000" | sudo tee /etc/zookeeper/conf/zoo.cfg',
			'echo "initLimit=10" | sudo tee -a /etc/zookeeper/conf/zoo.cfg',
	    	'echo "syncLimit=5" | sudo tee -a /etc/zookeeper/conf/zoo.cfg',
	    	'echo "dataDir=/var/lib/zookeeper" | sudo tee -a /etc/zookeeper/conf/zoo.cfg',
	    	'echo "clientPort=2181" | sudo tee -a /etc/zookeeper/conf/zoo.cfg',
			'echo "The Original zoo.cfg is kept safe at zoo.cfg.ori"',
			'echo "Setting Quorum"',
			'echo ' + quorum + ' | sudo tee /etc/mesos-master/quorum',
			'echo ' + conf['MASTERS'][i][ipaddr] + ' | sudo tee /etc/mesos-master/ip',
			'sudo cp /etc/mesos-master/ip /etc/mesos-master/hostname'
			'echo "Configuring Marathon"',
			'sudo mkdir -p /etc/marathon/conf',
			'sudo cp /etc/mesos-master/hostname /etc/marathon/conf',
			'sudo cp /etc/mesos/zk /etc/marathon/conf/master',
			'echo "zk://' + zkaddr + '/marathon" | sudo tee /etc/marathon/conf/zk'])

		for j in xrange(mctr):
			ret = subprocess.call(['ssh','root@' + hostname,
	    		'echo "server.' + conf['MASTERS'][j]['id'] + '=' + conf['MASTERS'][j]['ipaddr'] + ':2888:3888" | sudo tee -a /etc/zookeeper/conf/zoo.cfg'])

	for i in xrange(mctr):
        hostname = str(conf['MASTERS'][i]['name']) + '.' + str(args.domain)
        print "Start Mesos-Master Service on " + hostname + "..."

		ret = subprocess.call(['ssh','root@' + hostname,
			'sudo stop mesos-slave',
	    	'echo manual | sudo tee /etc/init/mesos-slave.override',
	    	'sudo restart zookeeper',
	    	'sudo start mesos-master',
		    'sudo start marathon'])

	for i in xrange(sctr):
		hostname = str(conf['SLAVES'][i]['name']) + '.' + str(args.domain)
        print "Accessing " + hostname + " over ssh..."
		ret = subprocess.call(['ssh','root@' + hostname,
			'echo "Adding Mesosphere Repository"',
			'sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF',
			'DISTRO=$(lsb_release -is | tr "[:upper:]" "[:lower:]")',
			'CODENAME=$(lsb_release -cs)',
			'echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list',
			'sudo apt-get -y update',
			'echo "Installing Mesos"',
			'sudo apt-get -y install mesos=0.26*',
			'echo "Configuring Zookeeper"',
			'echo "zk://' + zkaddr + '/mesos" | sudo tee /etc/mesos/zk'])

	for i in xrange(sctr):
		hostname = str(conf['SLAVES'][i]['name']) + '.' + str(args.domain)
	    print "Start Mesos-Slave Service on " + hostname + "..."

		ret = subprocess.call(['ssh','root@' + hostname,
			'sudo stop zookeeper',
    		'echo manual | sudo tee /etc/init/zookeeper.override',
    		'echo manual | sudo tee /etc/init/mesos-master.override',
    		'sudo stop mesos-master',
    		'echo ' + conf['SLAVES'][i]['ipaddr'] + ' | sudo tee /etc/mesos-slave/ip',
    		'sudo cp /etc/mesos-slave/ip /etc/mesos-slave/hostname',
    		'sudo start mesos-slave'])
