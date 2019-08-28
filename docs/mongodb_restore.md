How to: Restore the MongoDB database
====
The clowder database is the database where the 4CeeD data is kept.

## Requirements

You will need:
- MongoDB utilities compatible with the version of MongoDB running in the MongoDB container: mainly mongorestore
- A mongodump of your database that you need to restore, please refer to [Backing up the MongoDB database](mongodb_backup.md)
- The IP address of the container running MongoDB

## Restoring the database

1. Download the mongodb utilities that are compatible with the version of MongoDB running in the container.
If you need to know what version you are running please refer to the **"What version of MongoDB do I have?"** section of  [Backing up the MongoDB database](mongodb_backup.md).

2. If this is a new instance of 4CeeD, then you can restore the dump right into the new database. However if this is an exsisting server you need to power down the stack, and move, rename, or delete the previous database. If you have the room on the disk I suggest you just mv the directory to something like originalDB_bad. 

To find where your MongoDB database location is look for the Mongodb section in the **4ceedframework/docker-compose.yaml** file:

```
# Mongodb database used to store metadata/data
mongodb:
  image: mongo:3.2.1
  ports:
    - "127.0.0.1:27017:27017"
  volumes:
    - /srv/data/mongodb/data:/data/db
```

So for this instance I would rename `/srv/data/mongodb/data` to `/srv/data/mongodb/bad_data` 
Then I would recreate the `/srv/data/mongodb/data` directory for a fresh database to restore my dump into. Do not do this until you power down the 4CeeD Stack, which is coming up next:

3. Power down the 4CeeD stack
```
docker-compose down
```
4. Rename, delete, or move the original database directory and create a new one

5. Power up the 4CeeD stack
```
docker-compose up -d
```

6. Find out the IP address of the MongoDB instance with docker inspect and search for IP address with grep:

```
docker inspect 4ceedframework_mongodb_1 |grep -i ipaddress
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.4",
                    "IPAddress": "172.17.0.4",
```
OK, so now I know my MongoDB container is running on 172.17.0.4
You can also look for the port number but generally its going to be running on 27017

7. Craft the mongorestore statement.

The overall syntax of this command will be:

```
/PATH/TO/MONGORESTORE -h IP_ADDRESS_OF_MONGO_CONTAINER:27017 --DB clowder /PATH/TO/DUMP/FILE
```
So my command to restore an old version of the clowder mongodb database is:

```
/srv/4ceedframework/mongo3.2.1/bin/mongorestore -h 172.17.0.4:27017 --db clowder /home/rundblom/4CeeD-2019-07-11-1200/clowder
```
Now it is a good idea to restart the 4Ceed Stack and see if the MongoDB container has problems staying up.
If the MongoDB container looks stable: attempt to login to the 4CeeD web interface. Hopefully the database restore is a success!

