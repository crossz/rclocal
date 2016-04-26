#!/bin/sh
. /etc/profile.d/caiex.sh
. /opt/sbcconsumer/profile.d/caiex_matlab.sh
exec java -jar /opt/sbcconsumer/SBC-MAT-1.0.jar >> /opt/logs/sbcconsumer.out 2>&1 
