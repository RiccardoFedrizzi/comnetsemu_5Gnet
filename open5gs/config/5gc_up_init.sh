#!/bin/bash

if [[ -z "$COMPONENT_NAME" ]]; then
	echo "Error: COMPONENT_NAME environment variable not set"; exit 1;

elif [[ "$COMPONENT_NAME" =~ ^upf_cld$ ]]; then
    ip tuntap add name ogstun mode tun
    ip addr add 10.45.0.1/16 dev ogstun
    ip link set ogstun up
    iptables -t nat -A POSTROUTING -s 10.45.0.1/16 ! -o ogstun -j MASQUERADE

    iperf3 -B 10.45.0.1 -s -fm &

    cp /open5gs/install/etc/open5gs/temp/upf_cld.yaml /open5gs/install/etc/open5gs/upf.yaml 

elif [[ "$COMPONENT_NAME" =~ ^upf_mec$ ]]; then
    ip tuntap add name ogstun mode tun
    ip addr add 10.46.0.1/16 dev ogstun
    ip link set ogstun up
    iptables -t nat -A POSTROUTING -s 10.46.0.1/16 ! -o ogstun -j MASQUERADE

    iperf3 -B 10.46.0.1 -s -fm &

    cp /open5gs/install/etc/open5gs/temp/upf_mec.yaml  /open5gs/install/etc/open5gs/upf.yaml 

else
	echo "Error: Invalid component name: '$COMPONENT_NAME'"
fi

sleep 15
./install/bin/open5gs-upfd
