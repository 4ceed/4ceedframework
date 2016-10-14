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
	echo "Deploying 4CeeD's dependent tools..."
	# Deploy RabbitMQ
	$KUBECTL create -f tools/rabbitmq/rabbitmq-controller.yaml
	$KUBECTL create -f tools/rabbitmq/rabbitmq-service.yaml

	# Deploy MongoDB 
	$KUBECTL create -f tools/mongodb/mongo-controller.yaml
	$KUBECTL create -f tools/mongodb/mongo-service.yaml

	# Deploy Elasticsearch 
	$KUBECTL create -f tools/elasticsearch/service-account.yaml
	$KUBECTL create -f tools/elasticsearch/es-rc.yaml
	$KUBECTL create -f tools/elasticsearch/es-svc.yaml 
fi

# Setup 4CeeD curator 
if [ "$TARGET" == "curator" ] || [ "$TARGET" == "all" ]; then
	echo "Deploying 4CeeD's curator..."

	# Deploy curator to Kubernetes:
	$KUBECTL create -f curator/curator-rc.yaml
	$KUBECTL create -f curator/curator-svc.yaml
fi


# Setup extractors
if [ "$TARGET" == "extractors" ] || [ "$TARGET" == "all" ]; then
	echo "Deploying 4CeeD's extractors..."
	$KUBECTL create -f extractors/
fi

# Setup 4CeeD's uploader 
if [ "$TARGET" == "uploader" ] || [ "$TARGET" == "all" ]; then
	echo "Deploying 4CeeD's uploader..."

	# Deploy curator to Kubernetes:
	$KUBECTL create -f uploader/uploader-rc.yaml
	$KUBECTL create -f uploader/uploader-svc.yaml
fi
