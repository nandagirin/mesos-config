#!/bin/bash -xe
echo "***************************************************************"
echo "** Running version: Ubuntu 16.04 LTS                         **"
echo "***************************************************************"
echo "Configuring $1 as Mesos master server"
echo "Set variables"
echo "Installing dependencies"
sudo dpkg --configure -a
sudo apt update
sudo apt -y upgrade
sudo apt install -y tar wget git
sudo apt install -y autoconf libtool python-software-properties debconf-utils
sudo apt install -y build-essential python-dev python-six python-virtualenv libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev zlib1g-dev iputils-ping
echo "Installing dependency: Oracle Java 8"
sudo apt-add-repository -y ppa:webupd8team/java
sudo apt -y update
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections
sudo apt -y install oracle-java8-installer
echo "Installing Mesosphere"
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
CODENAME=$(lsb_release -cs)
echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list
sudo apt -y update
sudo apt -y install mesos marathon
echo "Configuring Zookeeper"
echo $2 | sudo tee /etc/mesos/zk
echo $3 | sudo tee /etc/zookeeper/conf/myid
echo "Overwrite zoo.cfg"
sudo cp /etc/zookeeper/conf/zoo.cfg /etc/zookeeper/conf/zoo.cfg.ori
sudo cp /tmp/zoo.cfg /etc/zookeeper/conf/
echo "The Original zoo.cfg is kept safe at zoo.cfg.ori"
echo "Setting Mesos-Master"
echo $4 | sudo tee /etc/mesos-master/quorum
echo $5 | sudo tee /etc/mesos-master/ip
echo $1 | sudo tee /etc/mesos-master/hostname
echo "Configuring Marathon"
echo "MARATHON_MASTER=$2" | sudo tee /etc/default/marathon
echo "MARATHON_ZK=$6" | sudo tee -a /etc/default/marathon
echo "Start Mesos Service"
sudo systemctl stop mesos-slave.service
if [ $7 -eq 0 ]
then
    echo manual | sudo tee /etc/init/mesos-slave.overr3e
fi
sudo systemctl restart zookeeper.service
sudo systemctl restart mesos-master.service
sudo systemctl restart marathon.service
sudo apt -y autoremove
sudo rm -rf /tmp/*