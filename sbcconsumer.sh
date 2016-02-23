#!/bin/sh
. /etc/profile
nohup java -jar /opt/sbcconsumer/SBC-0.0.1-SNAPSHOT.jar > /opt/logs/sbcconsumer_nohup.out &

