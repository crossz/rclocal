#!/bin/sh
. /etc/profile
exec python /opt/rclocal/oltp-notify.py >> /opt/logs/oltpnotify.out 2>&1
