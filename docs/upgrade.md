Upgrade 4CeeD Components
====

You can upgrade 4CeeD's components individually by simply pointing to a new version of component's Docker image. For example, to upgrade [4CeeD Uploader](https://github.com/4ceed/4ceeduploader):

- First, pull the latest version of the Uploader,  build its Docker image, and push it to Docker Hub (or your local Docker registry)
- Turn-off the current version of the Uploader:
```
./shutdown.sh uploader
```
- Update the version of Uploader's Docker image by modifying the file `uploader/uploader-rc.yaml` and change the following line to the appropriate version of the image:
```
image: t2c2/4ceeduploader
```
- Start the new Uploader:
```
./startup.sh uploader
```
