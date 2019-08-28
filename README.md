4CeeD Framework
====

4CeeD is a framework that supports **C**apture, **C**urate, **C**oordinate, **C**orrelate, and **D**istribute scientific data. For more information, visit 4CeeD's website at https://4ceed.github.io 

This repository consists of a collections of deployment scripts for various tools and components that make up the 4CeeD framework.

## 4CeeD In Action

Take a look at the following Youtube video to see how our scientific users use 4CeeD in real environment.

<a href="https://www.youtube.com/watch?v=ICDqsOGgwg0" target="_blank"><img src="docs/4ceed_video_thumbnail.jpg" border="1px" height="300px" align="middle" alt="4CeeD In Action"/></a>

## Setup
- [docker-compose](docs/docker_setup.md): Setup 4CeeD as a group of Docker containers running on a single machine. The most simple way to setup 4CeeD. Recommended for a quick test of 4CeeD functionalities.

## Legacy Setup Information
- [minikube](docs/minikube_setup.md): Recommended for a quick setup of 4CeeD running on Kubernetes environment.
- [Kubernetes](docs/kubernetes_setup.md): Setup 4CeeD on a Kubernetes cluster. Our recommended way to setup 4CeeD in production.
- [Google Cloud Platform](docs/gcp_setup.md): Setup 4CeeD on using Google Cloud Platform's Container Engine. 
- [Setup Kubernetes v1.6.6 on Ubuntu 16.04 LTS cluster](docs/k8s_setup_ubuntu.md)

## New Features - 2018/12
- [Updated dashboard/visualization]
- [Mobile view support]
- [Jupyter notebook integration]
- [Support for LDAP Authentication/CILogin]

## Other Resources
- [How to: Register extractors](docs/register_extractors.md)
- [How to: Run 4CeeD in persistent mode](docs/persistent_mode.md) 
- [How to: Access 4CeeD using a DNS name](docs/domain_name.md) 
- [How to: Upgrade 4CeeD components](docs/upgrade.md) 
- [How to: Roll back a 4Ceed component](docs/rollback_component.md)
- [How to: Backup the MongoDB database](docs/mongodb_backup.md)
- [How to: Restore the MongoDB database](docs/mongodb_restore.md)


## Contact

Feel free to open issues or create pull requests. Please [join 4CeeD's Slack channel](https://join.slack.com/t/4ceed/shared_invite/MjMyMDIyMDc2OTc4LTE1MDM2OTYzODUtNWU3ZWQ5Yzc1OA) if you have any question.
