#!/bin/bash -xe
clear
echo "***************************************************************"
echo "** Running version: Ubuntu 16.04 LTS                         **"
echo "***************************************************************"
echo "Configuring $HOSTNAME as Mesos master server"
echo "Installing dependencies"
sudo apt update
sudo apt install -y tar wget git
sudo apt install -y autoconf libtool
sudo apt -y install build-essential python-dev python-six python-virtualenv libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev zlib1g-dev iputils-ping
echo "Installing dependency: Oracle Java 8"
sudo apt-add-repository ppa:webupd8team/java
sudo apt -y update
sudo apt -y install oracle-java8-installer
echo "Installing Mesosphere"
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
CODENAME=$(lsb_release -cs)
echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list
sudo apt -y update
sudo apt -y install zookeeper mesos marathon
echo "Configuring Zookeeper"
echo $ZKADDRESS | sudo tee /etc/mesos/zk
echo $ID | sudo tee /etc/zookeeper/conf/myid
echo "Overwrite zoo.cfg"
sudo cp /etc/zookeeper/conf/zoo.cfg /etc/zookeeper/conf/zoo.cfg.ori
echo "tickTime=2000" | sudo tee /etc/zookeeper/conf/zoo.cfg
echo "initLimit=10" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
echo "syncLimit=5" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
echo "dataDir=/var/lib/zookeeper" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
echo "clientPort=2181" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
echo $ZOOCFG | sudo tee -a /etc/zookeeper/conf/zoo.cfg
echo "The Original zoo.cfg is kept safe at zoo.cfg.ori"
echo "Setting Mesos-Master"
echo $QUORUM | sudo tee /etc/mesos-master/quorum
echo $IP | sudo tee /etc/mesos-master/ip
echo $HOSTNAME | sudo tee /etc/mesos-master/hostname
echo "Configuring Marathon"
echo "MARATHON_MASTER=$ZKADDRESS" | sudo tee -a /etc/default/marathon
echo "MARATHON_ZK=$ZKMARATHON" | sudo tee -a /etc/default/marathon
echo "Start Mesos Service"
sudo systemctl stop mesos-slave
if [$CHECK -eq 0]
then
    echo manual | sudo tee /etc/init/mesos-slave.override
fi
sudo systemctl restart zookeeper
sudo systemctl restart mesos-master
sudo systemctl restart marathon