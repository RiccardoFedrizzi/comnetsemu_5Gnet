#!/bin/bash

docker exec -it $(docker ps -aq -f "name=open5gs_UP") /bin/bash

