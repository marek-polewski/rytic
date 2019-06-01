#!/bin/bash

set -e

PROJECT="527460643857.dkr.ecr.eu-west-1.amazonaws.com/meme-server:master"

# first login your docker to ECR
aws ecr get-login --no-include-email | bash


# build docker image
docker build --tag "$PROJECT" .

# create ecr repo on aws
# using gui or cli or sdk

# push your image to ACCOUNDID.dkr.ecr.eu-west-1.amazonaws.com/


docker push "$PROJECT"
