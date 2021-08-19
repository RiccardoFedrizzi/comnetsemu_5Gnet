#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

from dotenv import load_dotenv, dotenv_values

if __name__ == "__main__":

    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    prj_folder="/home/vagrant/ccn_project/comnetsemu_5Gnet"

    env = dotenv_values( prj_folder + "/.env")

    net = Containernet(controller=Controller, link=TCLink)

    info("*** Add controller\n")
    net.addController("c0")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1")

    info("*** Adding Host for open5gs CP\n")
    cp = net.addDockerHost(
        "cp",
        dimage="my5gc",
        ip="192.168.0.111/24",
        # dcmd="",
        dcmd="/open5gs/install/etc/open5gs/5gc_cp_init.sh",
        docker_args={
            "ports" : { "3000/tcp": 3000 },
            "volumes": {
                prj_folder + "/log": {
                    "bind": "/open5gs/install/var/log/open5gs",
                    "mode": "rw",
                },
                prj_folder + "/mongodbdata": {
                    "bind": "/var/lib/mongodb",
                    "mode": "rw",
                },
                prj_folder + "/open5gs/config": {
                    "bind": "/open5gs/install/etc/open5gs",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
            },
        },
    )

    info("*** Adding open5gs_UP\n")
    env["COMPONENT_NAME"]="upf"
    up = net.addDockerHost(
        "upf",
        dimage="my5gc",
        ip="192.168.0.112/24",
        # dcmd="",
        dcmd="/open5gs/install/etc/open5gs/temp/5gc_up_init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/log": {
                    "bind": "/open5gs/install/var/log/open5gs",
                    "mode": "rw",
                },
                prj_folder + "/open5gs/config": {
                    "bind": "/open5gs/install/etc/open5gs/temp",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
            },
            "cap_add": ["NET_ADMIN"],
            "sysctls": {"net.ipv4.ip_forward": 1},
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding gNB\n")
    env["COMPONENT_NAME"]="ueransim-gnb-1"
    gnb = net.addDockerHost(
        "gnb", 
        dimage="myueransim",
        ip="192.168.0.131/24",
        # dcmd="",
        dcmd="/mnt/ueransim/open5gs_gnb_init.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding UE\n")
    env["COMPONENT_NAME"]="ueransim-ue-1"
    ue = net.addDockerHost(
        "ue", 
        dimage="myueransim",
        ip="192.168.0.132/24",
        # dcmd="",
        dcmd="/mnt/ueransim/open5gs_ue_init_single_pdu.sh",
        docker_args={
            "environment": env,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/etc/timezone": {
                    "bind": "/etc/timezone",
                    "mode": "ro",
                },
                "/etc/localtime": {
                    "bind": "/etc/localtime",
                    "mode": "ro",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )

    info("*** Adding link\n")
    net.addLink(cp, s1,  bw=1000, delay="1ms", intfName1="cp-s1",  intfName2="s1-cp")
    net.addLink(up, s1,  bw=1000, delay="1ms", intfName1="up-s1",  intfName2="s1-up")
    net.addLink(gnb, s1, bw=1000, delay="1ms", intfName1="gnb-s1", intfName2="s1-gnb")
    net.addLink(ue, s1,  bw=1000, delay="1ms", intfName1="ue-s1",  intfName2="s1-ue")

    info("\n*** Starting network\n")
    net.start()

    if not AUTOTEST_MODE:
        # spawnXtermDocker("open5gs")
        # spawnXtermDocker("gnb")
        CLI(net)

    net.stop()
