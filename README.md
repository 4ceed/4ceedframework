4CeeD Framework
====

4CeeD is a framework that supports **C**apture, **C**urate, **C**oordinate, **C**orrelate, and **D**istribute scientific data. For more information, visit 4CeeD's website at https://4ceed.github.io 

This repository consists of a collections of deployment scripts for various tools and components that make up the 4CeeD framework.

## Prerequisites
- Minikube: For Quickstart guide
- Kubernetes: We have tested Kubernetes with the following configurations: `KUBE_VERSION=1.3.7`, `FLANNEL_VERSION=0.5.5`, and `ETCD_VERSION=2.3.1`. Tested version of Docker is `1.9.1` or later. Make sure you setup Kubernetes with the right set of components. 

## Quick start
To quickly test 4CeeD framework, we recommend to use a local setup of Kubernetes using [minikube](https://github.com/kubernetes/minikube). To setup a minikube cluster on a local computer, follow [minikube's setup instructions](http://kubernetes.io/docs/getting-started-guides/minikube/).

### Start 4CeeD
After installing minikube, start a minikube cluster:

```
minikube start
```

Before starting 4CeeD services, modify `custom.conf` file to customize new your 4CeeD instance. For the quick start with minikube, you only need to modify `ADMIN_EMAIL` and `SMTP_SERVER` to update your own orignazation information. Please note that `SMTP_SERVER` needs to be a valid SMTP server so that registration verification emails can be sent when users sign-up.

After that, run `./reconf.sh` to refresh the configuration. Then, start all 4CeeD services by running the following command:
```
./startup.sh all
```

Wait until all 4CeeD services start (this process can take a while since it will require downloading a bunch of Docker images from Docker Hub). To check the status of all services, use the following command and make sure that all pods have status `Running`:

```
kubectl get pods --namespace=4ceed
```

### Access 4CeeD
When all servies have started, we can access 4CeeD Curator at `http://192.168.99.100:32500`, and 4CeeD Uploader at `http://192.168.99.100:32000/4ceeduploader/`. Please note that `192.168.99.100` is the default IP address of minikube node. To obtain this address, run `minikube ip`.

Please note that the first user that can sign-up to the system has to be the user with email in `ADMIN_EMAIL`.

### Stop 4CeeD
To stop all services, run the following command:
```
./shutdown.sh all
```

## Setup 4CeeD on a baremetal cluster

This guide is recommended for more advanced users with Linux and cluster setup experience.

First, you will need to have Kubernetes setup on a baremetal cluster. Pick your own solution [here](http://kubernetes.io/docs/getting-started-guides/#bare-metal) (we have tested on [Ubuntu](http://kubernetes.io/docs/getting-started-guides/ubuntu/) cluster). 

Next, update configuration in `custom.conf` according to your Kubernetes setup:

* `KUBECTL`: Path to `kubectl` command
* `MONGODB_IP`, `RABBITMQ_IP`, `ELASTICSEARCH_IP`: IP addresses of services based on your cluster IP range setup
* `CURATOR_ADDR`, `UPLOADER_ADDR`: Addresses of the Curator and Uploader 

Then, run `./reconf.sh` to refresh configuration information.

After that, you can follow remaining steps that are similar to ones in Quick start. Please note that 4CeeD curator is now running at: `$CURATOR_ADDR`, and 4CeeD Uploader is now running at: `$UPLOADER_ADDR`.

## Upgrade 4CeeD Components

You can upgrade 4CeeD's components individually by simply pointing to a new version of component's Docker image. For example, to upgrade [4CeeD Uploader](https://github.com/4ceed/4ceeduploader):

- First, pull the latest version of the Uploader,  build its Docker image, and push it to Docker Hub (or your local Docker registry)
- Turn-off the current version of the Uploader:
```
./shutdown.sh uploader
```
- Update the version of Uploader's Docker image by modifying the file `uploader/uploader-rc.yaml` and change the following line to the appropriate version of the image:
```
image: t2c2/4ceeduploader
```
- Start the new Uploader:
```
./startup.sh uploader
```

## Contact

Feel free to create an issue or pull request. Please contact Phuong Nguyen (pvnguye2 at illinois dot edu) if you have any question.
