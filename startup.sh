#!/bin/bash

# Setup environment variables
export KUBECTL=/home/phuong/kubernetes/cluster/ubuntu/binaries/kubectl
BUILD_DOCKER_IMG="false"

# Setup tools
echo "Deploying 4CeeD's dependent tools..."
cd tools
./tools-deploy.sh

# Setup 4CeeD curator 
echo "Deploying 4CeeD's curator..."
cd ../curator 
./curator-deploy.sh $BUILD_DOCKER_IMG


# Setup 4CeeD's uploader 
echo "Deploying 4CeeD's uploader..."
cd ../uploader 
./uploader-deploy.sh $BUILD_DOCKER_IMG
