#!/bin/sh
. /etc/profile
#exec nohup java -javaagent:/opt/apache-tomcat-7.0.63/OneAPM/oneapm.jar -jar GAME-SERVICE-1.0.jar >> /opt/games/logs/gameser.log 2>&1 & 
exec java -jar /opt/games/GAME-SERVICE-1.0.jar >> /opt/games/logs/gameser.log 2>&1  
