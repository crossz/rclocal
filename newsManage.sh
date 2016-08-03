#!/bin/sh
. /etc/profile
nohup java -jar /opt/apps/newsManage-1.0-SNAPSHOT.war --server.port=8814 &

