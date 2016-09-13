#!/bin/bash

# Clone the latest version of 4CeeD curator:
# git clone https://bitbucket.org/todd_n/4ceedcurator.git

# Copy necessary files to 4ceedcurator folder:
cp Dockerfile curator-start.sh libjnotify64.so 4ceedcurator/
mv 4ceedcurator/libjnotify64.so 4ceedcurator/libjnotify.so

# Build 4CeeD curator Docker image and push to Docker Hub:
docker build -t t2c2/4ceedcurator 4ceedcurator/
docker push t2c2/4ceedcurator

# Deploy curator to Kubernetes:
$KUBECTL create -f curator-rc.yaml
$KUBECTL create -f curator-svc.yaml
