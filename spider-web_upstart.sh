#!/bin/sh
#. /etc/profile.d/caiex.sh

java -jar /opt/spider/spider-web.war >> /opt/logs/spider-web.out
