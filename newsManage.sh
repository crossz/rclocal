#!/bin/sh
. /etc/profile
nohup java -jar newsManage-1.0-SNAPSHOT.war --server.port=8814 &

