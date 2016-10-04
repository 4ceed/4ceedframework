#!/bin/bash

source custom.conf

# Setup environment variables
export KUBECTL
$KUBECTL delete namespace 4ceed

# Shutdown 4CeeD's uploader 
echo "Shutting down 4CeeD's uploader..."
$KUBECTL delete svc t2c2uploadersvc
$KUBECTL delete rc t2c2uploader

# Shutdown 4CeeD's curator 
echo "Shutting down 4CeeD's curator..."
$KUBECTL delete svc t2c2curatorsvc
$KUBECTL delete rc t2c2curator

# Extractors
echo "Shutting down 4CeeD's extractors..."
$KUBECTL delete rc dm3-extractor
$KUBECTL delete rc image-preview-extractor
$KUBECTL delete rc sem-extractor
$KUBECTL delete rc xray-extractor

# Setup tools
echo "Shutting down 4CeeD's dependent tools..."
$KUBECTL delete svc elasticsearch 
$KUBECTL delete rc es 
$KUBECTL delete svc mongo 
$KUBECTL delete rc mongo-controller 
$KUBECTL delete svc rabbitmq-service 
$KUBECTL delete rc rabbitmq-controller 
