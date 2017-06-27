Setup 4CeeD on Google Cloud Platform (GCP)
====

## Prerequisites

- Setup a [Google Cloud Platform](https://cloud.google.com/) account.
- Create a [container enginer](https://cloud.google.com/container-engine/) cluster.
- Install [Google Cloud SDK](https://cloud.google.com/sdk/) that provide Command-Line Interface to access GCP.
- Install [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Connect to GCP cluster

- Configure kubectl command line access by running the following command:
```
gcloud container clusters get-credentials [CLUSTER_NAME] --zone [ZONE_NAME] --project [PROJECT_NAME]
```
- (Optional) You can also start a proxy to connect to the Kubernetes control plane:
```
kubectl proxy
```
Then, open the Kubernetes's Dashboard interface by navigating to the following location in your browser `http://localhost:8001/ui`  

## Configure 4CeeD to run on GCP

- Since each GCP cluster has its own IP address range, we need to update the IP addresses of 4CeeD services (located in `custom.conf` file) to be compatible with the new GCP cluster’s IP range.

For example, if the cluster has the IP range of `10.4.0.0/14`, we can set the IP addresses of 4CeeD services as follow:

```
ELASTICSEARCH_IP=10.7.255.22
MONGODB_IP=10.7.255.33
RABBITMQ_IP=10.7.255.44
```

- Configure admin email address `ADMIN_EMAIL` (and SMTP server address `SMTP_SERVER`, in case email verification is required) in `custom.conf`.

- Setup new [static external IP address](https://cloud.google.com/compute/docs/configure-ip-addresses#before-you-begin) on GCP and assign the static IP to a running VM instance in the cluster

- To enable external access to 4CeeD, we need to create a [firewall rule](https://cloud.google.com/compute/docs/vpc/using-firewalls#creating_firewall_rules) to allow external access to 4CeeD at port 32500 (i.e., 4CeeD's default port).

- After updating configurations, run `./reconf.sh` to apply the new configurations.

## Deploy 4CeeD on GCP

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
When all servies have started, we can access 4CeeD at `http://[STATIC_IP_ADDRESS]:32500`, where `STATIC_IP_ADDRESS` is the static IP acquired from the previous step.

Please note that the first user that can sign-up to the system has to be the user with email in `ADMIN_EMAIL`.

### Stop 4CeeD
To stop all services, run the following command:
```
./shutdown.sh all
```
