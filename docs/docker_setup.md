Setup 4CeeD using Docker Compose
====

## Prerequisites

For this type of deployment, we need [Docker](https://www.docker.com/get-docker) and [docker-compose](https://docs.docker.com/compose/). Particularly, 4CeeD Framework is deployed as a set of services running as Docker containers on a single machine. Since this is a non-Kubernetes setup, you will not get the benefits supported by Kubernetes, such as fault tolerance and easy scaling of applications.

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

## Clear cached data of stopped containers

Please notice that, `docker-compose` caches data of the stopped containers for the next run. To clear the cached data, run the following command:

```
docker-compose rm
```

*Note: This command will NOT remove the data from persistent volume as described in previous section.*