#!/bin/bash

export DB_URI="mongodb://localhost/open5gs"

mongod --smallfiles --dbpath /var/lib/mongodb --logpath /open5gs/install/var/log/open5gs/mongodb.log --logRotate reopen --logappend --bind_ip_all &


sleep 10 && cd webui && npm run dev &

./install/bin/open5gs-nrfd & 
sleep 5
./install/bin/open5gs-smfd &
./install/bin/open5gs-amfd & 
./install/bin/open5gs-ausfd &
./install/bin/open5gs-udmd &
./install/bin/open5gs-udrd &
./install/bin/open5gs-pcfd &
./install/bin/open5gs-bsfd &
./install/bin/open5gs-nssfd


