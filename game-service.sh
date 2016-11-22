#!/bin/sh
. /etc/profile
exec java -jar /opt/GAMES/GAME-SERVICE-1.0.jar >> /opt/logs/game-service.out 2>&1
