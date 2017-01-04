#!/bin/sh
#export http_proxy=http://188.166.174.133:33128
cd /opt/spider
exec phantomjs /opt/spider/500.js 0 utf-8 >> /opt/logs/w500.log 2>&1

