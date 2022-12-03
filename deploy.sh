#!/bin/bash -e

# Deploy to heroku and Cloud Function on commits of master branch
TAG=$(versioningit)
# Deploy to docker hub new version (tag)
echo Deploy to docker hub
echo $DOCKER_PASSWORD |
docker login -u $DOCKER_USERNAME --password-stdin
docker tag $DOCKER_USERNAME/$DOCKER_REPO{,:$TAG}
docker push $DOCKER_USERNAME/$DOCKER_REPO:$TAG
docker push $DOCKER_USERNAME/$DOCKER_REPO:latest
