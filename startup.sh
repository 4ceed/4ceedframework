#!/bin/bash

# Setup environment variables
source custom.conf
export KUBECTL

# Get startup target
if [ "$1" == "all" ] || [ "$1" == "tools" ] || [ "$1" == "extractors" ] || \
   [ "$1" == "curator" ] || [ "$1" == "uploader" ]; then
	TARGET="$1"
else
	echo 'Invalid startup target (all|tools|extractors|curator|uploader).'
	exit 1
fi

# Create 4ceed namespace
$KUBECTL create namespace 4ceed

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
	$KUBECTL create -f extractors/xray-powder-extractor.yaml
	$KUBECTL create -f extractors/afm-extractor.yaml
	$KUBECTL create -f extractors/zip-extractor.yaml
	sleep 5
fi

# Setup 4CeeD's uploader 
if [ "$TARGET" == "uploader" ] || [ "$TARGET" == "all" ]; then
    echo
	echo "========Deploying 4CeeD's uploader...========"
	echo

	# Deploy curator to Kubernetes:
	$KUBECTL create -f uploader/uploader-rc.yaml
	$KUBECTL create -f uploader/uploader-svc.yaml
fi
