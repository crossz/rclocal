#!/bin/sh
. /etc/profile.d/caiex.sh
. /opt/sbcconsumer/profile.d/caiex_matlab.sh
nohup java -jar /opt/sbcconsumer/SBC-0.0.1-SNAPSHOT.jar > /opt/logs/sbcconsumer_nohup.out &

