Setup Kubernetes v1.6.6 on Ubuntu 16.04 LTS Cluster
====

## Step 0 - Prepraration
- This guide assumes that you have already had a set of machines installed with Ubuntu 16.04 LTS and these machines all have access to the Internet & can see each other.

## Step 1 - Install Docker, Kubeadm, and Kubelet
- *Note*: Run this step run on all nodes.
- Install `docker-engine` (in particular, Docker version 1.11.2) instead of the default `docker-ce`:

First, cleanup existing installation:
```
sudo apt-get purge docker-ce 
```

Then, update package list:
```
sudo -i
apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
```

Finally, install docker-engine:
```
sudo apt-get install docker-engine
```
Make sure that Docker's version is `1.11.2` by running `docker version`.

Another option to install `docker-engine` is via installing `.deb` binary file:
```
wget -O docker.deb https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_1.11.2-0~xenial_amd64.deb
sudo dpkg -i docker.deb
```

- Install `kubeadm` (v1.6.6) and `kubelet` (v1.6.6): 

First, cleanup existing installations:
```
sudo apt-get purge kubeadm
sudo apt-get purge kubelet
```

Then, install the specific version of `kubeadm` & `kubelet`:
```
sudo apt-get install -y kubelet=1.6.6-00 kubeadm=1.6.6-00
```

## Step 2 - Initialize Kubernetes on the Master node using Kubeadm
- *Note*: Run this step on the master node only.
- Run the following command to initialize Kubernetes (add option `--pod-network-cidr` to use `flannel`-based networking):
```
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --kubernetes-version=v1.6.6
```

- Then, run the following commands to initialize kubernetes context for the current user:
```
sudo cp /etc/kubernetes/admin.conf $HOME/ 
sudo chown $(id -u):$(id -g) $HOME/admin.conf
export KUBECONFIG=$HOME/admin.conf
```
 
Please note that the third command (i.e., `export KUBECONFIG=$HOME/admin.conf`) can be put into current user's startup shell scripts (e.g., `~/.bashrc` in case of Bash) for future use.

- Next, install pod networking plugin (used to allow pods to communicate with each other), for example, using `weave` (which we found works well in our setup):
```
kubectl apply -f https://git.io/weave-kube-1.6 
```

Or, using `flannel`:
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel-rbac.yml
```

- Finally, run the following command to allow scheduler to schedule pods on master node:
```
kubectl taint nodes --all node-role.kubernetes.io/master-
```

## Step 3 - Join worker nodes
- *Note*: Run this step on each worker node.
- The output of the `kubeadm init` command in Step 2 should include a command to join worker nodes. For example:
``` 
sudo kubeadm join --token TOKEN_KEY 172.22.246.122:6443
```

(`TOKEN_KEY` can also be obtained by running `sudo kubeadm token list`)

- Run the above command on every worker node to join the node to Kubernetes cluster.

- After a while, you can run `kubectl get nodes` on master node to make sure that all nodes have joined the cluster.

## Other notes

- For debugging, check `kubelet`'s logs at `/var/log/syslog`
- Using `kubeadm`, all Kubernetes services, like apiserver, proxy, flannel, etc. are running as containers in kube-system namespace. Checkout the configuration of those services in `/etc/kubernetes/manifests/` & check their logs by using `kubectl logs` command.