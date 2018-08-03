#!/bin/sh
clear
echo "*************************************************************************"
echo "** Running version: Ubuntu 14.04 LTS                                   **"
echo "** This configuration is ONLY for ONE Master                           **"
echo "** Further modification is required for multiple MASTERs               **"
echo "*************************************************************************"
read -p "Install and configure mesos master in $HOSTNAME? [Y/y] to proceed: " yn
case $yn in
  [Yy]* )
    echo "Use the IP list for your reference"
    ifconfig | grep "inet addr"
    echo "Enter the IP address of this server"
    read -p "Slave IP: " SLAVE_IP
    echo "Enter the master IP address for this slave"
    read -p "Master IP: " MASTER_IP
    echo "Configuring $SLAVE_IP as a slave for $MASTER_IP"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
    DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
    CODENAME=$(lsb_release -cs)
    echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list
    sudo apt-get -y update
    sudo apt-get -y install mesos
    echo "zk://$MASTER_IP:2181/mesos" | sudo tee /etc/mesos/zk
    sudo stop zookeeper
    echo manual | sudo tee /etc/init/zookeeper.override
    echo manual | sudo tee /etc/init/mesos-master.override
    sudo stop mesos-master
    echo $SLAVE_IP | sudo tee /etc/mesos-slave/ip
    sudo cp /etc/mesos-slave/ip /etc/mesos-slave/hostname
    sudo start mesos-slave
    ;;
  * )
    echo "Retreat"
    ;;
esac
