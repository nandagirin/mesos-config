#!/bin/bash -xe
echo "***************************************************************"
echo "** Running version: Ubuntu 16.04 LTS                         **"
echo "***************************************************************"
echo "Configuring $HOSTNAME as Mesos slave server"
echo "Installing dependencies"
if [ $CHECK -eq 0 ]
then
    sudo apt update
    sudo apt install -y tar wget git
    sudo apt install -y autoconf libtool
    sudo apt install -y build-essential python-dev python-six python-virtualenv libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev zlib1g-dev iputils-ping
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
    sudo apt -y install zookeeper mesos
fi
echo "Configuring Zookeeper for Mesos Slave"
echo $ZKADDRESS | sudo tee /etc/mesos/zk
echo "Configurng Mesos slave"
echo $IP | sudo tee /etc/mesos-slave/ip
echo $HOSTNAME | sudo tee /etc/mesos-slave/hostname
echo "docker,mesos" | sudo tee /etc/mesos-slave/containerizers
echo "5mins" | sudo tee /etc/mesos-slave/executor_registration_timeout
echo '"ports:[1-65000]"' | sudo tee /etc/mesos-slave/resources
if [ $CHECK -eq 0 ]
then
    echo manual | sudo tee /etc/init/mesos-master.override
    sudo systemctl stop mesos-master
fi
sudo sytemctl stop zookeeper
echo manual | sudo tee /etc/init/zookeeper.override
sudo systemctl restart mesos-slave