#!/bin/bash

docker exec -it $(docker ps -aq -f "name=ue") /bin/bash

