#!/bin/sh
cd /opt/spider/500
exec phantomjs /opt/spider/500/500.js 0 utf-8 >> /opt/logs/w500.log 2>&1

