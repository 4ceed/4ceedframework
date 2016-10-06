#!/bin/bash

# Setup environment variables
source custom.conf
export KUBECTL

# Create 4ceed namespace
$KUBECTL create namespace 4ceed

# Get startup target
if [ "$1" != "" ]; then
	if [ "$1" != "all" ] && [ "$1" != "tools" ] && [ "$1" != "extractors" ] && \
	   [ "$1" != "curator" ] && [ "$1" != "uploader" ]; then
		echo 'Invalid startup target (all|tools|extractors|curator|uploader).'
		exit 1
	else
		TARGET="$1"
	fi
else
    TARGET="all"
fi

# Setup tools
if [ "$TARGET" == "tools" ] || [ "$TARGET" == "all" ]; then
    echo
	echo "========Deploying 4CeeD's dependent tools...========"
	echo
	# Deploy RabbitMQ
	$KUBECTL create -f tools/rabbitmq/rabbitmq-controller.yaml
	$KUBECTL create -f tools/rabbitmq/rabbitmq-service.yaml
	sleep 5

	# Deploy MongoDB 
	$KUBECTL create -f tools/mongodb/mongo-controller.yaml
	$KUBECTL create -f tools/mongodb/mongo-service.yaml
	sleep 5

	# Deploy Elasticsearch 
	$KUBECTL create -f tools/elasticsearch/service-account.yaml
	$KUBECTL create -f tools/elasticsearch/es-rc.yaml
	$KUBECTL create -f tools/elasticsearch/es-svc.yaml 
	sleep 5
fi

# Setup 4CeeD curator 
if [ "$TARGET" == "curator" ] || [ "$TARGET" == "all" ]; then
    echo
	echo "========Deploying 4CeeD's curator...========"
	echo

	if [ "$BUILD_DOCKER_IMG" = "true" ]; then
		cd curator
		echo 'Building Curator Docker image from source...'
		# Clone the latest version of 4CeeD curator:
		git clone https://bitbucket.org/todd_n/4ceedcurator.git

		# Copy necessary files to 4ceedcurator folder:
		cp Dockerfile curator-start.sh libjnotify64.so 4ceedcurator/
		mv 4ceedcurator/libjnotify64.so 4ceedcurator/libjnotify.so

		# Build 4CeeD curator Docker image:
		docker build -t t2c2/4ceedcurator 4ceedcurator/
		cd ..
	else
		echo 'Using prebuilt Curator Docker image...'
	fi

	# Deploy curator to Kubernetes:
	$KUBECTL create -f curator/curator-rc.yaml
	$KUBECTL create -f curator/curator-svc.yaml
	sleep 5
fi


# Setup extractors
if [ "$TARGET" == "extractors" ] || [ "$TARGET" == "all" ]; then
    echo
	echo "========Deploying 4CeeD's extractors...========"
	echo

	$KUBECTL create -f extractors/dm3-extractor.yaml
	$KUBECTL create -f extractors/image-preview-extractor.yaml
	$KUBECTL create -f extractors/sem-extractor.yaml
	$KUBECTL create -f extractors/xray-extractor.yaml
	$KUBECTL create -f extractors/afm-extractor.yaml
	sleep 5
fi

# Setup 4CeeD's uploader 
if [ "$TARGET" == "uploader" ] || [ "$TARGET" == "all" ]; then
    echo
	echo "========Deploying 4CeeD's uploader...========"
	echo

	if [ "$BUILD_DOCKER_IMG" = "true" ]; then
		cd uploader
		echo 'Building Uploader Docker image from source...'
		# Clone the latest version of 4CeeD curator:
		git clone git@bitbucket.org:smkctk/4ceeduploader.git

		# Copy necessary files to 4ceedcurator folder:
		cp Dockerfile 4ceeduploader/

		# Build 4CeeD curator Docker image:
		docker build -t t2c2/4ceeduploader 4ceeduploader/
		cd ..
	else
		echo 'Using prebuilt Uploader Docker image...'
	fi

	# Deploy curator to Kubernetes:
	$KUBECTL create -f uploader/uploader-rc.yaml
	$KUBECTL create -f uploader/uploader-svc.yaml
fi
