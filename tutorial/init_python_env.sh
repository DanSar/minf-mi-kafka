#!/bin/bash

lib_dir=libs
env_name=kafka_env

# install librdkafka from repo
mkdir -p $lib_dir 
cd $lib_dir
git clone https://github.com/edenhill/librdkafka.git
cd librdkafka/
./configure
make
sudo make install

cd ../../ 

# create virtualenv and install python libs
python3.6 -m venv $env_name
source $env_name/bin/activate
# in requirements we need to set the installed path of librdkafka, see: https://github.com/confluentinc/confluent-kafka-python/issues/65
python3.6 -m pip install -r requirements.txt
