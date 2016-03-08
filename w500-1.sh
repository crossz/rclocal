#!/bin/sh
cd /opt/spider/500
exec phantomjs /opt/spider/500/500.js -1 utf-8 >> /opt/logs/w500_upstart.log 2>&1

