#!/bin/bash

set -eux -o pipefail

RANDOM_SUFFIX=$(echo $RANDOM | md5sum | head -c 20; echo;)
IMAGE_NAME="default-project:jenkins-$RANDOM_SUFFIX"

current_script=$(realpath "$0")
project_root=$(dirname $(dirname $current_script))

cd $project_root/ci

# build image for CI
docker build . \
    --build-arg USERID=$UID \
    --tag $IMAGE_NAME

# run container for tests
rm -f myproject/.gitkeep
docker run \
    --rm \
    -v /var/run/postgresql/:/var/run/postgresql/:rw \
    -v $project_root/ci/myproject:/ci/myproject:rw \
    --user $UID \
    $IMAGE_NAME

# check docker build for project
cd myproject

echo "[DOCKER] Run 'docker build'"
cd foo
npm install
# without buildkit you get file permission issues on the VOLUME instruction
# we also can't use docker-compose build since the compose version (1.21) is too old
# and COMPOSE_DOCKER_CLI_BUILD is only supported in docker-compose 1.25+
DOCKER_BUILDKIT=1 docker build .
