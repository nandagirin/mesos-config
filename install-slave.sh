#!/bin/bash -xe
echo "***************************************************************"
echo "** Running version: Ubuntu 16.04 LTS                         **"
echo "***************************************************************"
echo "Configuring $4 as Mesos slave server"
if [ $1 -eq 0 ]
then
    echo "Installing dependencies"
    sudo apt update
    sudo apt install -y tar wget git
    sudo apt install -y autoconf libtool
    sudo apt install -y build-essential python-dev python-six python-virtualenv libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev zlib1g-dev iputils-ping
    echo "Installing dependency: Oracle Java 8"
    sudo apt-add-repository -y ppa:webupd8team/java
    sudo apt -y update
    echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections
    sudo apt -y install oracle-java8-set-default
    echo "Installing Mesosphere"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
    DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
    CODENAME=$(lsb_release -cs)
    echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list
    sudo apt -y update
    sudo apt -y install zookeeper mesos
fi
echo "CHECK IF DOCKER IS INSTALLED"
if [ -x "$(command -v docker)" ]; then
    echo "Docker has been installed."
else
    echo "Docker has not been installed. Proceed to install Docker."
    sudo apt install \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo apt-key fingerprint 0EBFCD88
    sudo add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"
    sudo apt update
    sudo apt -y install docker-ce
    sudo usermod -aG docker $USER
fi
echo "Installing Docker"
echo "Configuring Zookeeper for Mesos Slave"
echo $2 | sudo tee /etc/mesos/zk
echo "Configurng Mesos slave"
echo $3 | sudo tee /etc/mesos-slave/ip
echo $4 | sudo tee /etc/mesos-slave/hostname
echo $5 | sudo tee /etc/mesos-slave/attributes
echo "ports:[1-65535]" | sudo tee /etc/mesos-slave/resources
echo "docker,mesos" | sudo tee /etc/mesos-slave/containerizers
echo "5mins" | sudo tee /etc/mesos-slave/executor_registration_timeout
if [ $1 -eq 0 ]
then
    echo manual | sudo tee /etc/init/mesos-master.override
    sudo systemctl stop mesos-master
    sudo sytemctl stop zookeeper
    echo manual | sudo tee /etc/init/zookeeper.override
fi
sudo systemctl restart mesos-slave
sudo apt -y autoremove
sudo rm -rf /tmp/*
echo 'ALL DONE :)'