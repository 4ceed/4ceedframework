#!/bin/bash

# Setup environment variables
export KUBECTL=/home/phuong/kubernetes/cluster/ubuntu/binaries/kubectl

# Setup tools
echo "Deploy 4CeeD's dependent tools..."
cd tools
./tools-deploy.sh

# Setup 4CeeD curator 
echo "Deploy 4CeeD's curator..."
cd ../curator 
./curator-deploy.sh


# Setup 4CeeD's uploader 
echo "Deploy 4CeeD's uploader..."
cd ../uploader 
./uploader-deploy.sh
