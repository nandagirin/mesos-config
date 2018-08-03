#!/bin/bash
echo 'This installation script is intended for Ubuntu 16.04'
apt-get update

OPENCV_VERSION=3.2.0
GPU=1

# Install dependencies
apt-get install -y build-essential cmake pkg-config libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libgtk2.0-dev libatlas-base-dev gfortran python2.7-dev git liblapacke-dev libopenblas-dev libprotobuf-dev python-pip libhdf5-dev libboost-dev libpython3-dev python3-pip

pip install numpy
pip3 install numpy


OPENCV_DIR=~/opencv
cd ~
if [ ! -d $OPENCV_DIR ]
then	
	git clone https://github.com/opencv/opencv.git
fi


cd opencv
git checkout $OPENCV_VERSION

# OPENCV_CONTRIB_DIR=~/opencv_contrib-$OPENCV_VERSION
# cd ~
# IFS='.' read -ra MAJOR_VERSION <<< "$OPENCV_VERSION"
# if [ ! -d $OPENCV_CONTRIB_DIR ]
# then
# 	if [ $MAJOR_VERSION == 3 ]
# 		then
#			addr=https://github.com/opencv/opencv_contrib/archive/
#			endfile=.zip
#
#			full_path=$addr$OPENCV_VERSION$endfile
#	
#			wget -O opencv_contrib.zip $full_path
#
#			unzip opencv_contrib.zip
#  	fi
# fi

# cd opencv

BUILD_DIR=build-$OPENCV_VERSION
if [ -d $BUILD_DIR ]
then
	rm -r $BUILD_DIR
fi

mkdir build-$OPENCV_VERSION

cd build-$OPENCV_VERSION

if [ $GPU==1 ]
then 
	GPUSTATS=ON
else
	GPUSTATS=OFF
fi

if [ $MAJOR_VERSION == 3 ]
then
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_CUDA=$GPUSTATS -D ENABLE_FAST_MATH=1 -D CUDA_FAST_MATH=$GPU -D WITH_CUBLAS=$GPU -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_FFMPEG=1 ..
	# cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_CUDA=$GPUSTATS -D ENABLE_FAST_MATH=1 -D CUDA_FAST_MATH=$GPU -D WITH_CUBLAS=$GPU -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_FFMPEG=1 -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-$OPENCV_VERSION/modules ..
else
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_CUDA=$GPUSTATS -D ENABLE_FAST_MATH=1 -D CUDA_FAST_MATH=$GPU -D WITH_CUBLAS=$GPU -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON ..
fi

make -j$(getconf _NPROCESSORS_ONLN)

make install

ldconfig