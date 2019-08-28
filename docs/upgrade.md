How to: Upgrade 4CeeD Components
====

You can upgrade 4CeeD's components individually by simply pointing to a new version of component's Docker image. For example, to upgrade 4CeeD Curator: 

First: Power down the 4ceed stack:
```
docker compose down
```
Second: Update the version of Curator's Docker image by modifying the file `docker-compose.yaml` and change the `VERSION_NUMBER` in following line to the new version of the image:
```
image: t2c2/4ceedcurator:VERSION_NUMBER
```
Third: Power up the 4ceed stack:
```
docker-compose up -d
```
