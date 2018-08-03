#!/bin/bash
echo 'This installation script is intended for Ubuntu 16.04'
apt-get update

# install dependencies
apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libsdl2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo wget zlib1g-dev libavresample-dev libx264-dev
mkdir ~/ffmpeg_sources

cd ~/ffmpeg_sources
wget http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz
tar xzvf yasm-1.3.0.tar.gz
cd yasm-1.3.0
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin"
make -j$(getconf _NPROCESSORS_ONLN)
make install

cd ~/ffmpeg_sources
wget http://www.nasm.us/pub/nasm/releasebuilds/2.13.01/nasm-2.13.01.tar.bz2
tar xjvf nasm-2.13.01.tar.bz2
cd nasm-2.13.01
./autogen.sh
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin"
PATH="$HOME/bin:$PATH" make -j$(getconf _NPROCESSORS_ONLN)
make install

# cd ~/ffmpeg_sources
# wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2
# tar xjvf last_x264.tar.bz2
# cd x264-snapshot*
# PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static --disable-opencl --enable-shared --extra-cflags="-fPIC"
# PATH="$HOME/bin:$PATH" make -j$(getconf _NPROCESSORS_ONLN)
# make install

# apt-get -y install cmake mercurial
# cd ~/ffmpeg_sources
# hg clone https://bitbucket.org/multicoreware/x265
# cd ~/ffmpeg_sources/x265/build/linux
# PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
# sudo make
# make install

# cd ~/ffmpeg_sources
# wget -O fdk-aac.tar.gz https://github.com/mstorsjo/fdk-aac/tarball/master
# tar xzvf fdk-aac.tar.gz
# cd mstorsjo-fdk-aac*
# autoreconf -fiv
# ./configure --prefix="$HOME/ffmpeg_build" --enable-shared --extra-cflags="-fPIC"
# #sudo make
# #make install

# cd ~/ffmpeg_sources
# wget http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
# tar xzvf lame-3.99.5.tar.gz
# cd lame-3.99.5
# ./configure --prefix="$HOME/ffmpeg_build" --enable-nasm --enable-shared --extra-cflags="-fPIC"
# #sudo make
# #make install

# cd ~/ffmpeg_sources
# wget https://archive.mozilla.org/pub/opus/opus-1.1.5.tar.gz
# tar xzvf opus-1.1.5.tar.gz
# cd opus-1.1.5
# ./configure --prefix="$HOME/ffmpeg_build" --enable-shared --extra-cflags="-fPIC"
# #sudo make
# #make install

# sudo apt-get install git
# cd ~/ffmpeg_sources
# git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git
# cd libvpx
# PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --enable-shared --extra-cflags="-fPIC"
# #sudo PATH="$HOME/bin:$PATH" make
# #make install

cd ~/ffmpeg_sources
wget http://ffmpeg.org/releases/ffmpeg-3.4.tar.bz2
tar xjvf ffmpeg-3.4.tar.bz2
mv ffmpeg-3.4 ffmpeg
cd ffmpeg
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$HOME/ffmpeg_build" --pkg-config-flags="--static" --extra-cflags="-I$HOME/ffmpeg_build/include" --extra-ldflags="-L$HOME/ffmpeg_build/lib" --extra-cflags="-fPIC" --bindir="$HOME/bin" --enable-gpl --enable-libx264 --enable-nonfree --enable-shared --enable-pic

PATH="$HOME/bin:$PATH" make -j$(getconf _NPROCESSORS_ONLN)

make install

hash -r

ln -s ~/ffmpeg_build/lib/* /usr/local/lib

ldconfig
