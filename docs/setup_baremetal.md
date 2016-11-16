Setup 4CeeD on Baremetal Cluster 
====

This guide is recommended for more advanced users with Linux and cluster setup experience.

First, you will need to have Kubernetes setup on a baremetal cluster. Pick your own solution [here](http://kubernetes.io/docs/getting-started-guides/#bare-metal) (we have tested on [Ubuntu](http://kubernetes.io/docs/getting-started-guides/ubuntu/) cluster). 

Next, update configuration in `custom.conf` according to your Kubernetes setup:

* `KUBECTL`: Path to `kubectl` command
* `MONGODB_IP`, `RABBITMQ_IP`, `ELASTICSEARCH_IP`: IP addresses of services based on your cluster IP range setup
* `CURATOR_ADDR`, `UPLOADER_ADDR`: Addresses of the Curator and Uploader 

Then, run `./reconf.sh` to refresh configuration information.

After that, you can follow remaining steps that are similar to ones in Quick start. Please note that 4CeeD curator is now running at: `$CURATOR_ADDR`, and 4CeeD Uploader is now running at: `$UPLOADER_ADDR`.

