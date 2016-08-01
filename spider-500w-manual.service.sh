#!/bin/sh
cd /opt/spider/w500-manual
exec phantomjs /opt/spider/500/500.js >> /opt/logs/w500.log 2>&1

