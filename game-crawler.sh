#!/bin/sh
. /etc/profile
exec java -jar /opt/games/GAME-CRAWLER-SERVICE-1.0.jar >> /opt/logs/game-craw.log 2>&1 & 
