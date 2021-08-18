#!/bin/bash

docker exec -it $(docker ps -aq -f "name=gnb") /bin/bash

