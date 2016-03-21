#!/bin/sh
. /etc/profile.d/caiex.sh
jstorm kill SequenceTest 10  >> /opt/logs/jstorm.out 2>&1 &
echo 'please wait for 10s'
sleep 10
