#!/bin/bash

# export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

sleep 25
./nr-ue -c /mnt/ueransim/open5gs-ue.yaml > /mnt/log/ue.log 2>&1
