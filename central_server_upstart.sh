#!/bin/sh
. /etc/profile
cd /opt/payoutcancel
exec python -m payoutcancel > /dev/null 2>&1
