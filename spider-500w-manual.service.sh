#!/bin/sh
cd /opt/spider/w500-manual
exec phantomjs /opt/spider/w500-manual/w500-manual.js >> /opt/logs/w500.log 2>&1

