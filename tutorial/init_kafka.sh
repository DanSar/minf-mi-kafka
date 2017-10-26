#!/bin/bash

mkdir ./logs
pip install kafka-python

kafka_home=/usr/local/kafka_2.11-0.11.0.1
kafka_bin="${kafka_home}/bin"
kafka_config="${kafka_home}/config"

##################
##################

# start zookeeper (new terminal)
echo ""
echo "stating zookeeper..."
x-terminal-emulator -e "${kafka_bin}/zookeeper-server-start.sh ${kafka_config}/zookeeper.properties"

sleep 4s

# start kafka (new terminal)
echo ""
echo "starting kafka server..."
x-terminal-emulator -e "${kafka_bin}/kafka-server-start.sh ${kafka_config}/server.properties"

##################
##################

## Tests
sleep 5s

# create twitter topic
echo ""
echo "creating topic..."
${kafka_bin}/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitter

# start test producer
echo ""
echo "stating test producer..."
x-terminal-emulator -e "python3 ./producer.py"

# start test consumer
echo ""
echo "starting consumer..."
echo ""
./test-consumer.sh
