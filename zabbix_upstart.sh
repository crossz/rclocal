#!/bin/bash
exec /opt/zabbix-2.2.2/sbin/zabbix_agentd start >> /tmp/zabbix_agentd.log 2>&1 
