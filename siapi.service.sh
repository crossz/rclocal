#!/bin/sh
. /etc/profile
cd /opt/apps/

java -jar CaiexOpenNewsApi-1.0-SNAPSHOT.jar >> /opt/logs/si-api.log 2>&1
