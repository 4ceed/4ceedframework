Quickstart: Setup 4CeeD Framework using Minikube
====

To quickly test 4CeeD framework, we recommend to use a local setup of Kubernetes using [minikube](https://github.com/kubernetes/minikube). To setup a minikube cluster on a local computer, follow [minikube's setup instructions](http://kubernetes.io/docs/getting-started-guides/minikube/).

## Start 4CeeD
After installing minikube, start a minikube cluster:

```
minikube start
```

Before starting 4CeeD services, modify `custom.conf` file to customize new your 4CeeD instance. For the quick start with minikube, you only need to modify `ADMIN_EMAIL` (and `SMTP_SERVER`, if email verification is required) to update your own information.

After that, run `./reconf.sh` to refresh the configuration. Then, start all 4CeeD services by running the following command:
```
./startup.sh all
```

Wait until all 4CeeD services start (this process can take a while since it will require downloading a bunch of Docker images from Docker Hub). To check the status of all services, use the following command and make sure that all pods have status `Running`:

```
kubectl get pods --namespace=4ceed
```

## Access 4CeeD
When all servies have started, we can access 4CeeD at `http://192.168.99.100:32500`. Please note that `192.168.99.100` is the default IP address of minikube node. To obtain this address, run `minikube ip`.

Please note that the first user that can sign-up to the system has to be the user with email in `ADMIN_EMAIL`.

## Stop 4CeeD
To stop all services, run the following command:
```
./shutdown.sh all
```
