#!/bin/bash

source custom.conf

# Setup environment variables
export KUBECTL

# Setup tools
echo "Deploying 4CeeD's dependent tools..."
cd tools
./tools-deploy.sh

# Setup 4CeeD curator 
echo "Deploying 4CeeD's curator..."
cd ../curator 
./curator-deploy.sh $REBUILD_IMAGES


# Setup 4CeeD's uploader 
echo "Deploying 4CeeD's uploader..."
cd ../uploader 
./uploader-deploy.sh $REBUILD_IMAGES
