#!/bin/bash

# Clone the latest version of 4CeeD curator:
# git clone https://bitbucket.org/todd_n/4ceeduploader.git

# Copy necessary files to 4ceedcurator folder:
cp Dockerfile 4ceeduploader/

# Build 4CeeD curator Docker image and push to Docker Hub:
docker build -t t2c2/4ceeduploader 4ceeduploader/
docker push t2c2/4ceeduploader

# Deploy curator to Kubernetes:
$KUBECTL create -f uploader-rc.yaml
$KUBECTL create -f uploader-svc.yaml
