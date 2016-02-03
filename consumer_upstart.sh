#!/bin/sh
exec java -jar /opt/consumer/oltp-service-consumer-1.0-SNAPSHOT.jar >> /opt/logs/consumer.out 2>&1

