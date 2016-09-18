#!/bin/sh -ex
service spider-robot restart
echo 'spider robot restart'
service spider-robot_stats restart
echo 'spider robot stats restart'
service spider-robot_500 restart
echo 'spider robot 500 restart'
service spider-robot_jbb restart
echo 'spider robot jbb restart'
service spider-robot_lj restart
echo 'spider robot lj restart'

service spider-robot_lj restart
echo 'spider robot clean restart'
service spider-robot_lj restart
echo 'spider robot manual restart'
