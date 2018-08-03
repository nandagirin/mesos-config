#!/env/bash

echo "Installing docker ..."

sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" >> /etc/apt/sources.list.d/docker.list
sudo apt-get update -y
sudo apt-get purge -y lxc-docker
sudo apt-cache policy docker-engine
sudo apt-get install -y linux-image-extra-$(uname -r)
sudo sudo apt-get install -y docker-engine
sudo docker run hello-world

echo "Finish installing docker ..."