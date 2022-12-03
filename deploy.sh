#!/bin/bash -e

TAG=$(versioningit)
# Deploy to docker hub new version (tag)
echo Deploy to docker hub new version GITHUB_REF=${GITHUB_REF}, TAG=$TAG,  GITHUB_REF_NAME=$GITHUB_REF_NAME
echo $DOCKER_PASSWORD |
docker login -u $DOCKER_USERNAME --password-stdin
docker tag $DOCKER_USERNAME/$DOCKER_REPO{,:$TAG}
docker push $DOCKER_USERNAME/$DOCKER_REPO:$TAG
docker push $DOCKER_USERNAME/$DOCKER_REPO:latest
