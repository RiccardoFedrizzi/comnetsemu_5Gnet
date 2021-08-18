#!/bin/bash

docker exec -it $(docker ps -aq -f "name=^$1$") /bin/bash

