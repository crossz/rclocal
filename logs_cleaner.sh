#!/bin/sh


delete_logs() {
    if [ -d $2 ];then
      cd $2
      find . -type f -name "$1" -exec rm -rf {} \;
    fi
}

# log parts

## sbc and sbcconsumer
delete_logs "$1" /opt/logs/sbc
delete_logs "$1" /opt/logs/sbcconsumer
delete_logs "$1" /opt/logs/sbcconsumer2/sbcconsumer

### oltp and oltp-dubbo and oltp-consumer
delete_logs "$1" /opt/logs/oltp-api
delete_logs "$1" /opt/logs/dubbo
delete_logs "$1" /opt/logs/consumer

## docker parts
docker rmi $(docker images -q -f dangling=true)
docker volume rm `docker volume ls -q -f dangling=true`

