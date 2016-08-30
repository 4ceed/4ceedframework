4CeeD Uploader Deployment
=====

## Preparation
Before deploying 4CeeD uploader, first check-out the latest version from BitBucket into `4ceeduploader/` directorty under project's root. After that, copy file `uploader-deploy/Dockerfile` into `4ceeduploader/` directory.

## Build 4CeeD Uploader Docker image
Next, build 4CeeD Uploader Docker image by running the following command under `4ceeduploader/`:
```
docker build -t t2c2/4ceeduploader .
```
And push the latest container image onto Docker hub:
```
docker push t2c2/4ceeduploader
```

## Deploy 4CeeD Uploader container on Kubernetes
After building uploader's container image, we can deploy 4CeeD Uploader on Kubernetes cluster. First, we create uploader service:
```
kubectl create -f uploader-deploy/uploader-svc.yaml
```

And then, create uploader's replication controller with default number of replicas is 1 (i.e., to run one instance of uploader):
```
kubectl create -f uploader-deploy/uploader-rc.yaml
```

After running these commands, the uploader can be accessible at `http://[Cluster Node IP]:32000/4ceeduploader/`, where `[Cluster Node IP]` is the IP address of any node in Kubernetes cluster. You can change the default port `32000` to other value in file `uploader-deploy/uploader-svc.yaml`.


