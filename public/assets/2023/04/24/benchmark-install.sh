#!/bin/bash
apt-get update
apt-get -y install git curl wget

# Sysbench
apt-get -y install make automake libtool pkg-config libaio-dev libmysqlclient-dev libssl-dev
git clone 'https://github.com/akopytov/sysbench'
cd sysbench
./autogen.sh
./configure
make -j
make install

# Basemark GPU
wget 'https://cdn.downloads.basemark.com/BasemarkGPU-linux-x64-1.2.3.tar.gz'

# Unigine Benchmark
wget 'https://assets.unigine.com/d/Unigine_Superposition-1.1.run'
wget 'https://assets.unigine.com/d/Unigine_Valley-1.0.run'
wget 'https://assets.unigine.com/d/Unigine_Heaven-4.0.run'
