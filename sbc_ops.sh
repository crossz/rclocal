#!/bin/sh
cd /opt/SbcOps/
#exec python /opt/SbcOps/initOddsServer.py
nohup python /opt/SbcOps/initOddsServer.py >> /opt/logs/sbcops.log 2>&1 &
