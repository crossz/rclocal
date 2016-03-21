#!/bin/sh
. /etc/profile
#jstorm jar /opt/jstorm/rm-0.0.1-SNAPSHOT.jar com.caiex.storm.TestStormStart test
jstorm jar /opt/deploy/jstorm/example/sequence_test/sequence-split-merge-1.1.0-jar-with-dependencies.jar com.alipay.dw.jstorm.example.sequence.SequenceTopology /opt/deploy/jstorm/example/sequence_test/conf.yaml >> /opt/logs/jstorm.out 2>&1 &
echo 'please wait for 30s'
sleep 30
