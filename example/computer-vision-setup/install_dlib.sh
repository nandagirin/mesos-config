#!/bin/bash
echo 'This installation script is intended for Ubuntu 16.04'

DLIB_VERSION=19.7


apt-get update

apt-get -y install build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev python-dev python-pip python3-dev python3-pip python-tk

sudo -H pip install numpy scipy matplotlib scikit-image scikit-learn

cd ~
wget http://dlib.net/files/dlib-$DLIB_VERSION.tar.bz2
tar xvf dlib-$DLIB_VERSION.tar.bz2
mv dlib-$DLIB_VERSION dlib
cd dlib/
mkdir build
cd build
cmake ..
cmake --build . --config Release
sudo make install
sudo ldconfig
cd ..

pkg-config --libs --cflags dlib-1

sudo -H python setup.py install
