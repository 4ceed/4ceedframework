#!/bin/bash

# Deploy RabbitMQ
$KUBECTL create -f rabbitmq/rabbitmq-controller.yaml
$KUBECTL create -f rabbitmq/rabbitmq-service.yaml

# Deploy MongoDB 
$KUBECTL create -f mongodb/mongo-controller.yaml
$KUBECTL create -f mongodb/mongo-service.yaml

# Deploy Elasticsearch 
$KUBECTL create -f elasticsearch/service-account.yaml
$KUBECTL create -f elasticsearch/es-rc.yaml
$KUBECTL create -f elasticsearch/es-svc.yaml 
