#!/bin/bash

source ../custom.conf
export KUBECTL

if [ "$1" != "" ]; then
	BUILD_DOCKER_IMG="$1"
else
	# Use prebuilt Docker image as default
	BUILD_DOCKER_IMG="false"
fi

if [ "$BUILD_DOCKER_IMG" = "true" ]; then
	echo 'Building Curator Docker image from source...'
	# Clone the latest version of 4CeeD curator:
	git clone https://bitbucket.org/todd_n/4ceedcurator.git

	# Copy necessary files to 4ceedcurator folder:
	cp Dockerfile curator-start.sh libjnotify64.so 4ceedcurator/
	mv 4ceedcurator/libjnotify64.so 4ceedcurator/libjnotify.so

	# Build 4CeeD curator Docker image:
	docker build -t t2c2/4ceedcurator 4ceedcurator/
else
	echo 'Using prebuilt Curator Docker image...'
fi

# Deploy curator to Kubernetes:
$KUBECTL create -f curator-rc.yaml
$KUBECTL create -f curator-svc.yaml
