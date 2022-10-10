#!/bin/bash

sudo mn -c

docker stop $(docker ps -aq)

docker container prune -f

if [ "$1" == "log" ]; then
    cd log && sudo rm *.log 
fi

sudo ip link delete s1-ue
sudo ip link delete s2-s3
sudo ip link delete s2-s1
sudo ip link delete gnb-s1
sudo ip link delete s1-gnb
sudo ip link delete s1-cp
sudo ip link delete gnb-s2
sudo ip link delete s2-gnb
sudo ip link delete s3-cp
sudo ip link delete s1-ue1
sudo ip link delete s1-ue2
sudo ip link delete s1-ue3
sudo ip link delete s2-upf_mec
sudo ip link delete s3-upf
sudo ip link delete s1-uegnb
