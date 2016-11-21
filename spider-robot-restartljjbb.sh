#!/bin/sh -ex
service spider-robot_jbb restart
echo 'spider robot jbb restart'
service spider-robot_lj restart
echo 'spider robot lj restart'

### manual robot+500
#service spider-robot_manual restart
#echo 'spider robot manual restart'
#systemctl restart spider-500w-manual

echo "--------==== All restarted ====--------"
