#!/bin/bash

# Deploy RabbitMQ
$KUBECTL create -f rabbitmq-controller.yaml
$KUBECTL create -f rabbitmq-service.yaml

# Deploy MongoDB 
$KUBECTL create -f mongo-controller.yaml
$KUBECTL create -f mongo-service.yaml

# Deploy Elasticsearch 
$KUBECTL create -f es-rc.yaml
$KUBECTL create -f es-svc.yaml 
