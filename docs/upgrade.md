Upgrade 4CeeD Components
====

You can upgrade 4CeeD's components individually by simply pointing to a new version of component's Docker image. For example, to upgrade 4CeeD Curator: 

- First, turn-off the current version of the Uploader:
```
./shutdown.sh curator 
```
- Update the version of Curator's Docker image by modifying the file `curator/curator-rc.yaml` and change the `VERSION_NUMBER` in following line to the new version of the image:
```
image: t2c2/4ceedcurator:VERSION_NUMBER
```
- Then, start the new Curator:
```
./startup.sh curator 
```
