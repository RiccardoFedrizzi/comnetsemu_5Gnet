#!/bin/bash

docker build --no-cache --force-rm -t my5gc_v2-4-4 --file ./Dockerfile_5gc .
docker build --no-cache --force-rm -t myueransim_v3-2-6 --file ./Dockerfile_ueransim .
