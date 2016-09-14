#!/bin/bash

# Setup environment variables
export KUBECTL=/home/phuong/kubernetes/cluster/ubuntu/binaries/kubectl

# Shutdown 4CeeD's uploader 
echo "Shutdown 4CeeD's uploader..."
$KUBECTL delete svc t2c2uploadersvc
$KUBECTL delete rc t2c2uploader

# Shutdown 4CeeD's curator 
echo "Shutdown 4CeeD's curator..."
$KUBECTL delete svc t2c2curatorsvc
$KUBECTL delete rc t2c2curator

# Setup tools
echo "Shutdown 4CeeD's dependent tools..."
$KUBECTL delete svc elasticsearch 
$KUBECTL delete rc es 
$KUBECTL delete svc mongo 
$KUBECTL delete rc mongo-controller 
$KUBECTL delete svc rabbitmq-service 
$KUBECTL delete rc rabbitmq-controller 
