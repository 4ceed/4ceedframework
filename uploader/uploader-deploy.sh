#!/bin/bash

if [ "$1" != "" ]; then
	BUILD_DOCKER_IMG="$1"
else
	# Use prebuilt Docker image as default
	BUILD_DOCKER_IMG="false"
fi

if [ "$BUILD_DOCKER_IMG" = "true" ]; then
	echo 'Building Uploader Docker image from source...'
	# Clone the latest version of 4CeeD curator:
	git clone https://bitbucket.org/todd_n/4ceeduploader.git

	# Copy necessary files to 4ceedcurator folder:
	cp Dockerfile 4ceeduploader/

	# Build 4CeeD curator Docker image and push to Docker Hub:
	docker build -t t2c2/4ceeduploader 4ceeduploader/
	docker push t2c2/4ceeduploader
else
	echo 'Using prebuilt Uploader Docker image...'
	# Deploy curator to Kubernetes:
	$KUBECTL create -f uploader-rc.yaml
	$KUBECTL create -f uploader-svc.yaml
fi
