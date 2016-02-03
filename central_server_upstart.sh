#!/bin/sh
cd /opt/hadoop/centralrpc/
exec python /opt/hadoop/centralrpc/central_server.py >> /opt/logs/centralserver.out 2>&1
