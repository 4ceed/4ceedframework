Setup 4CeeD on Kubernetes Cluster 
====

*Disclaimer*: This is the recommended way to setup 4CeeD. This setup requires advanced users with Linux and cluster setup experience.

## Setup your own Kubernetes cluster

We have [tested on Ubuntu](https://kubernetes.io/docs/getting-started-guides/ubuntu/manual/) (14.04 LTS) cluster with the following version configurations: `KUBE_VERSION=1.3.7`, `FLANNEL_VERSION=0.5.5`, and `ETCD_VERSION=2.3.1`. Tested version of Docker is `1.9.1` or later. Make sure you use appropriate [releases](https://github.com/kubernetes/kubernetes/releases) of Kubernetes with the right set of configuration. 

To setup Kubernetes on other operating systems, pick your own Kubernetes deployment solution [here](https://kubernetes.io/docs/setup/pick-right-solution/). 

## Configure 4CeeD

Next, update configuration in `custom.conf` according to your Kubernetes setup:

* `KUBECTL`: Path to `kubectl` command
* `MONGODB_IP`, `RABBITMQ_IP`, `ELASTICSEARCH_IP`: IP addresses of services based on your cluster IP range setup
* `CURATOR_ADDR`: Addresses of the Curator and Uploader 

Then, run `./reconf.sh` to refresh configuration information.

## Deploy 4CeeD on Kubernetes cluster

### Start 4CeeD 

Start all 4CeeD services by running the following command:
```
./startup.sh all
```

Wait until all 4CeeD services start (this process can take a while since it will require downloading a bunch of Docker images from Docker Hub). To check the status of all services, use the following command and make sure that all pods have status `Running`:

```
kubectl get pods --namespace=4ceed
```

### Access 4CeeD
When all servies have started, we can access 4CeeD at `$CURATOR_ADDR` as configured in `custom.conf`.

Please note that the first user that can sign-up to the system has to be the user with email in `ADMIN_EMAIL`.

### Stop 4CeeD
To stop all services, run the following command:
```
./shutdown.sh all
```

