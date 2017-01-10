#!/bin/sh -ex

cd /opt/logs
rm -rf sbcconsumer.out.201*
rm -rf catalina-api.out.201*
rm -rf catalina-sbc.out.201*
rm -rf dubbo.out.201*
rm -rf consumer.out.201*

rm -rf centralserver.out.201*
rm -rf spider-web.out.201*

cd /opt/logs/spider-robot
rm -rf *.log.201*


