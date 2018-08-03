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
    read -p "Master IP: " MASTER_IP
    echo "Configuring $MASTER_IP as a MASTER"
    echo "Installing Dependency: Oracle Java 8"
    sudo apt-add-repository ppa:webupd8team/java
    sudo apt-get -y update
    sudo apt-get -y install oracle-java8-installer
    echo "Installing Mesosphere"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
    DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
    CODENAME=$(lsb_release -cs)
    echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list
    sudo apt-get -y update
    sudo apt-get -y install mesosphere
    echo "Configuring Zookeeper"
    echo "zk://$MASTER_IP:2181/mesos" | sudo tee /etc/mesos/zk
    echo 1 | sudo tee /etc/zookeeper/conf/myid
    echo "Overwrite zoo.cfg"
    zoocfg="/etc/zookeeper/conf/zoo.cfg.ori"
    if [-f "$zoocfg"]
    then
      echo "Original zoo.cfg is already stored"
    else
      sudo cp /etc/zookeeper/conf/zoo.cfg /etc/zookeeper/conf/zoo.cfg.ori
    fi
    echo "tickTime=2000" | sudo tee /etc/zookeeper/conf/zoo.cfg
    echo "initLimit=10" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
    echo "syncLimit=5" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
    echo "dataDir=/var/lib/zookeeper" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
    echo "clientPort=2181" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
    echo "server.1=$MASTER_IP:2888:3888" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
    echo "The Original zoo.cfg is kept safe at zoo.cfg.ori"
    echo "Setting Quorum"
    echo 1 | sudo tee /etc/mesos-master/quorum
    echo $MASTER_IP | sudo tee /etc/mesos-master/ip
    sudo cp /etc/mesos-master/ip /etc/mesos-master/hostname
    echo "Configuring Marathon"
    sudo mkdir -p /etc/marathon/conf
    sudo cp /etc/mesos-master/hostname /etc/marathon/conf
    sudo cp /etc/mesos/zk /etc/marathon/conf/master
    echo "zk://$MASTER_IP:2181/marathon" | sudo tee /etc/marathon/conf/zk
    echo "Start Mesos Service"
    sudo stop mesos-slave
    echo manual | sudo tee /etc/init/mesos-slave.override
    sudo restart zookeeper
    sudo start mesos-master
    sudo start marathon
    ;;
  * )
    echo "Retreat"
    ;;
esac
