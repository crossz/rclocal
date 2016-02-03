#!/bin/sh
exec java -jar /opt/dubbo/oltp-service-dubbo-1.0-SNAPSHOT.jar >> /opt/logs/dubbo.out 2>&1
