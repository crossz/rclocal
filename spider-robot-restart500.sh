#!/bin/sh -ex

service spider-robot_500 restart
echo 'spider robot 500 restart'

systemctl restart spider-500w
systemctl restart spider-500w-1
echo 'spider phantom 500 restart'

## manual robot
#service spider-robot_manual restart
#echo 'spider robot manual restart'
#systemctl restart spider-500w-manual

### clean robot
#service spider-robot_clean restart
#echo 'spider robot clean restart'

echo "--------==== All restarted ====--------"
