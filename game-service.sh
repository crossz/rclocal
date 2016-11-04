#!/bin/sh
. /etc/profile
exec java -jar /opt/games/GAME-SERVICE-1.0.jar >> /opt/logs/games/game-serv.log 2>&1 & 
