#!/bin/sh
cp /opt/logs/catalina-sbc.out /opt/logs/catalina-sbc.out.$(date +%Y%m%d) && cat /dev/null > /opt/logs/catalina-sbc.out
cp /opt/logs/catalina-api.out /opt/logs/catalina-api.out.$(date +%Y%m%d) && cat /dev/null > /opt/logs/catalina-api.out
cp /opt/logs/dubbo.out /opt/logs/dubbo.out.$(date +%Y%m%d) && cat /dev/null > /opt/logs/dubbo.out
cp /opt/logs/consumer.out /opt/logs/consumer.out.$(date +%Y%m%d) && cat /dev/null > /opt/logs/consumer.out
cp /opt/logs/sbcconsumer.out /opt/logs/sbcconsumer.out.$(date +%Y%m%d) && cat /dev/null > /opt/logs/sbcconsumer.out
cp /opt/logs/centralserver.out /opt/logs/centralserver.out.$(date +%Y%m%d) && cat /dev/null > /opt/logs/centralserver.out
cp /opt/logs/spider-web.out /opt/logs/spider-web.out.$(date +%Y%m%d) && cat /dev/null > /opt/logs/spider-web.out
