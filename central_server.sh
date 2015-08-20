#!/bin/sh
cd /opt/hadoop/centralrpc/

nohup python /opt/hadoop/centralrpc/central_server.py >> /opt/logs/central_server.log 2>&1 &
