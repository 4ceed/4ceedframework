Setup 4CeeD using Docker Compose
====

For this type of deployment, we use [docker-compose](https://docs.docker.com/compose/) to deploy 4CeeD Framework as a set of services running as Docker containers on a single machine. Since this is a non-Kubernetes setup, you will not get the benefits supported by Kubernetes, such as fault tolerance and easy scaling of applications.

The `docker-compose`'s definitions of 4CeeD Framework is located in `docker-compose.yml` file. Update `docker-compose.yml` with your own configuration information (e.g., `ADMIN_EMAIL`, `SMTP_SERVER`, etc.) before startup.

To start 4CeeD Framework, simply run the following command:

```
docker-compose up
```

After all services have been started, 4CeeD's curator is accessible at `http://[MACHINE_IP]:9000/`, where `[MACHINE_IP]` is the IP address of the machine on which `docker-compose` runs.
