#!/bin/bash

ip tuntap add name ogstun mode tun
ip addr add 10.45.0.1/16 dev ogstun
ip link set ogstun up
iptables -t nat -A POSTROUTING -s 10.45.0.1/16 ! -o ogstun -j MASQUERADE

# ip tuntap add name ogstun2 mode tun
# ip addr add 192.168.101.1/24 dev ogstun2
# ip link set ogstun2 up

# iptables -t nat -A POSTROUTING -s 192.168.101.0/24 ! -o ogstun2 -j MASQUERADE

sleep 15
./install/bin/open5gs-upfd


