Setup 4CeeD using Docker Compose on CentOS 7
====

## Prerequisites

For this type of deployment, we need [Docker](https://www.docker.com/get-docker) and [docker-compose](https://docs.docker.com/compose/). Particularly, 4CeeD Framework is deployed as a set of services running as Docker containers on a single machine. Since this is a non-Kubernetes setup, you will not get the benefits supported by Kubernetes, such as fault tolerance and easy scaling of applications.

enum34 is required for 4ceed, the easiest way to install enum34 is via pip:

```
pip install --upgrade enum34
```

## Setup 4CeeD

*Note: The following commands are run under the project's root directory.*

The `docker-compose`'s definitions of 4CeeD Framework is located in `docker-compose.yml` file. Update `docker-compose.yml` with your own configuration information (e.g., `ADMIN_EMAIL`, `SMTP_SERVER`, etc.) before startup.

To start 4CeeD Framework, simply run the following command:

```
docker-compose pull && docker-compose up
```

or in detached mode:

```
docker-compose pull && docker-compose up -d
```

After all services have been started, 4CeeD's curator is accessible at `http://[MACHINE_IP]:9000/`, where `[MACHINE_IP]` is the IP address of the machine on which `docker-compose` runs. Normally, this IP address can be obtained by running command `ifconfig` on Linux & Mac, or `ipconfig` on Windows. For extractors to work properly, please DO NOT use `127.0.0.1` or `localhost` as IP address for 4CeeD. 

To stop all services, simply press `Ctrl+C`, or run `docker-compose down` if running in detached mode.

## Setup persistent mode for MongoDB

By default, 4CeeD runs in non-persistent mode (i.e., data is lost after Docker is restarted, or container cache is cleared). To run 4CeeD in persistent mode, mount a local folder (using absolute path - e.g., `/absolute/path/to/mongodb/data`) to a volume for MongoDB service (e.g., `/data/db`) so that MongoDB's data is stored persistently in your specied local folder. In particular, add the following lines to MongoDB service definition in `docker-compose.yml`: 

```
  volumes:
    - /absolute/path/to/mongodb/data:/data/db
```

## Scale extractors

You can scale the number of replicas of each extractor by using `docker-compose scale` command. For example, to set 3 replicas for `dm3-extractor`, run the following command:

```
docker-compose scale dm3-extractor=3
``` 

We recommend that you increase the number of replicas for popularly used extractors to provide redundancy.

## Clear cached data of stopped containers

Please notice that, `docker-compose` caches data of the stopped containers for the next run. To clear the cached data, run the following command:

```
docker-compose rm
```

*Note: This command will NOT remove the data from persistent volume as described in previous section.*
Now is an excellent time to configure access to 4ceed via http (80) or https (443) 
[domain name](docs/domain_name.md)
