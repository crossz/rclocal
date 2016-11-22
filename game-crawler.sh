#!/bin/sh
. /etc/profile
exec java -jar /opt/GAMES/GAME-CRAWLER-SERVICE-1.0.jar >> /opt/logs/game-crawler.out 2>&1
