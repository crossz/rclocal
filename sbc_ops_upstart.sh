#!/bin/sh
. /etc/profile
cd /opt/SbcOps/
exec python /opt/SbcOps/initOddsServer.py >> /opt/logs/sbcops.out 2>&1
#nohup python /opt/SbcOps/initOddsServer.py >> /opt/logs/sbcops.log 2>&1 &
