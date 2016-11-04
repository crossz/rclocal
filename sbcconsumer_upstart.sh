#!/bin/sh
. /etc/profile
. /opt/SBCCONSUMER/profile.d/caiex_matlab.sh

exec java -jar /opt/SBCCONSUMER/SBC-MAT-1.0.jar >> /opt/logs/sbcconsumer.out 2>&1
