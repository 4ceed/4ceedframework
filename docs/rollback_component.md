How to: Roll back a 4CeeD component
====
Lets say you try a new version of the curator but it does not work: you can roll it back fairly easily.

In our scenario we wanted to upgrade to version 2019.06.15 of the curator, but something is wrong and we need
to go back to the previous version, and... we forgot what version that was.

## What versions of the images do we have?
We can see the versions of the docker images we have by running

``` 
docker image ls

REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
docker.io/rabbitmq                        latest              83878773002b        13 days ago         147 MB
docker.io/t2c2/4ceedcurator               2019.06.15          4fd04b988464        2 months ago        277 MB
docker.io/elasticsearch                   2                   5e9d896dc62c        11 months ago       479 MB
docker.io/t2c2/sem-extractor              18.05.29            9437c93405bb        15 months ago       684 MB
docker.io/t2c2/zip-extractor              18.05.28            cb3baa52e524        15 months ago       684 MB
docker.io/t2c2/4ceedcurator               18.01.29            a5e7cd6ec384        19 months ago       1.07 GB
docker.io/t2c2/dm3-extractor              latest              ff468ac774a6        19 months ago       790 MB
docker.io/t2c2/xray-extractor             latest              705ab1727924        21 months ago       833 MB
docker.io/t2c2/rutherford-spe-extractor   latest              b14128ebbcf7        22 months ago       833 MB
docker.io/t2c2/rutherford-nra-extractor   latest              408abd9e7b55        23 months ago       833 MB
docker.io/t2c2/afm-extractor              latest              8549e0973c3f        2 years ago         858 MB
docker.io/t2c2/image-preview-extractor    latest              450392569cc1        2 years ago         779 MB
docker.io/t2c2/xray-powder-extractor      latest              31048a609c9f        2 years ago         822 MB
docker.io/mongo                           3.2.1               7e350b877a9a        3 years ago         317 MB
```

Ah, so we have version 2019.06.15 and version 18.01.29 so the previous version was probably 18.01.29
So, lets shut down the rest of the 4ceed stack:

```
docker-compose down
Stopping 4ceedframework_zip-extractor_1            ... done
Stopping 4ceedframework_sem-extractor_1            ... done
Stopping 4ceedframework_image-preview-extractor_1  ... done
Stopping 4ceedframework_dm3-extractor_1            ... done
Stopping 4ceedframework_rutherford-spe-extractor_1 ... done
Stopping 4ceedframework_xray-extractor_1           ... done
Stopping 4ceedframework_afm-extractor_1            ... done
Stopping 4ceedframework_xray-powder-extractor_1    ... done
Stopping 4ceedframework_rutherford-nra-extractor_1 ... done
Stopping 4ceedframework_elasticsearch_1            ... done
Stopping 4ceedframework_rabbitmq_1                 ... done
Stopping 4ceedframework_mongodb_1                  ... done
Removing 4ceedframework_zip-extractor_1            ... done
Removing 4ceedframework_sem-extractor_1            ... done
Removing 4ceedframework_image-preview-extractor_1  ... done
Removing 4ceedframework_dm3-extractor_1            ... done
Removing 4ceedframework_rutherford-spe-extractor_1 ... done
Removing 4ceedframework_xray-extractor_1           ... done
Removing 4ceedframework_afm-extractor_1            ... done
Removing 4ceedframework_xray-powder-extractor_1    ... done
Removing 4ceedframework_rutherford-nra-extractor_1 ... done
Removing 4ceedframework_elasticsearch_1            ... done
Removing 4ceedframework_rabbitmq_1                 ... done
Removing 4ceedframework_mongodb_1                  ... done
```

Lets now change the version of the extractor in `docker-compose.yaml` to 4ceedcurator:18.01.29:

```
# 4CeeD framework 
4ceed:
  image: t2c2/4ceedcurator:18.01.29
  environment:
    CLOWDER_CONTEXT: "/"
```

Now lets start the 4ceed stack:

```
docker-compose up -d
Creating 4ceedframework_xray-powder-extractor_1    ... done
Creating 4ceedframework_xray-extractor_1           ... done
Creating 4ceedframework_image-preview-extractor_1  ... done
Creating 4ceedframework_rutherford-spe-extractor_1 ... done
Creating 4ceedframework_rutherford-nra-extractor_1 ... done
Creating 4ceedframework_dm3-extractor_1            ... done
Creating 4ceedframework_afm-extractor_1            ... done
Creating 4ceedframework_rutherford-spe-extractor_1 ... 
Creating 4ceedframework_4ceed_1                    ... done
Creating 4ceedframework_xray-extractor_1           ... 
Creating 4ceedframework_4ceed_1                    ... 
Creating 4ceedframework_sem-extractor_1            ... done
Creating 4ceedframework_zip-extractor_1            ... done
```

Lets make sure the docker containers are running:

```
docker-compose ps
4ceedframework_4ceed_1                      /clowder/curator-start.sh        Up      0.0.0.0:9000->9000/tcp                            
4ceedframework_afm-extractor_1              /code/extractor-start.sh         Up                                                        
4ceedframework_dm3-extractor_1              /code/extractor-start.sh         Up                                                        
4ceedframework_elasticsearch_1              /docker-entrypoint.sh elas ...   Up      9200/tcp, 9300/tcp                                
4ceedframework_image-preview-extractor_1    /code/extractor-start.sh         Up                                                        
4ceedframework_mongodb_1                    /entrypoint.sh mongod            Up      127.0.0.1:27017->27017/tcp                        
4ceedframework_rabbitmq_1                   docker-entrypoint.sh rabbi ...   Up      15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 5672/tcp
4ceedframework_rutherford-nra-extractor_1   /code/extractor-start.sh         Up                                                        
4ceedframework_rutherford-spe-extractor_1   /code/extractor-start.sh         Up                                                        
4ceedframework_sem-extractor_1              /code/extractor-start.sh         Up                                                        
4ceedframework_xray-extractor_1             /code/extractor-start.sh         Up                                                        
4ceedframework_xray-powder-extractor_1      /code/extractor-start.sh         Up                                                        
4ceedframework_zip-extractor_1              /code/extractor-start.sh         Up                                                        
```

Things are looking good, now try to log into your 4ceed installation
