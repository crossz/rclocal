#!/bin/sh

nohup storm jar /opt/rm.jar com.caiex.storm.StormStart > /opt/logs/storm_nohup.out &

