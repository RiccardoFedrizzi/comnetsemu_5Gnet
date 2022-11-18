#!/bin/bash

docker pull rfed/my5gc_v2-4-4
docker pull rfed/myueransim_v3-2-6

docker tag rfed/my5gc_v2-4-4       my5gc_v2-4-4
docker tag rfed/myueransim_v3-2-6  myueransim_v3-2-6