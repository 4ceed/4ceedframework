#!/bin/bash

# Setup environment variables
source custom.conf
export KUBECTL

# Get startup target
if [ "$1" == "all" ] || [ "$1" == "tools" ] || [ "$1" == "extractors" ] || \
   [ "$1" == "curator" ] ; then
	TARGET="$1"
else
	echo 'Invalid startup target (all|tools|extractors|curator).'
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
	$KUBECTL create -f tools/rabbitmq/rabbitmq-rc.yaml
	$KUBECTL create -f tools/rabbitmq/rabbitmq-svc.yaml
	sleep 5

	# Deploy MongoDB 
	$KUBECTL create -f tools/mongodb/mongodb-rc.yaml
	$KUBECTL create -f tools/mongodb/mongodb-svc.yaml
	sleep 5

	# Deploy Elasticsearch 
	$KUBECTL create -f tools/elasticsearch/service-account.yaml
	$KUBECTL create -f tools/elasticsearch/elasticsearch-rc.yaml
	$KUBECTL create -f tools/elasticsearch/elasticsearch-svc.yaml 
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
	$KUBECTL create -f extractors/rutherford-spe-extractor.yaml
	$KUBECTL create -f extractors/rutherford-nra-extractor.yaml
	sleep 5
fi
