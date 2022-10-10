#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

from python_modules.Open5GS   import Open5GS

import json, time

if __name__ == "__main__":

    prj_folder="/home/vagrant/comnetsemu/app/comnetsemu_5Gnet"
    
    print(f"*** Open5GS: Init subscriber for UE 0")
    o5gs   = Open5GS( "172.17.0.2" ,"27017")
    o5gs.removeAllSubscribers()
    with open( prj_folder + "/python_modules/subscriber_profile_1.json" , 'r') as f:
        profile = json.load( f )
    o5gs.addSubscriber(profile)

