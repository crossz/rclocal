#!/bin/sh
. /etc/profile
exec java -jar /opt/apps/newsManage-1.0-SNAPSHOT.war --server.port=8814 >> /opt/logs/news/newsManage.out 2>&1  

