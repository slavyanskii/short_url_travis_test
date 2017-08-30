#!/bin/bash

CONTAINER='app.server';

set -ex
docker exec -it ${CONTAINER} python /home/app/run_migrations.py;
echo 'Restarting container'
docker restart ${CONTAINER}