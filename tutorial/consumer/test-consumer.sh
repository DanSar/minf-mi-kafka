#!/bin/bash

kafka_home=/usr/local/kafka_2.11-0.11.0.1

echo "Listining for topic..."
${kafka_home}/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic halloween --from-beginning
