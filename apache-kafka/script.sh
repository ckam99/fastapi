#!/usr/bin/env bash



echo "kafka is running"
( 
    cd /opt/kafka
    bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
    while [! nc -z localhost 2181]
    do
      sleep 1; 
    done
    bin/kafka-server-start.sh config/server.properties
)

