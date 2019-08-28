How to: Backup the MongoDB database
====
The **clowder** database is the database where the 4CeeD data is kept.

## Requirements

You will need:
- MongoDB utilities compatible with the version of MongoDB running in the MongoDB container: mainly mongodump

## What version of MongoDB do I have?
How do I find out what version of MongoDB I am running?
Method #1 
Look for what MongoDB docker image you have:
```
docker image ls
docker.io/mongo                           3.2.1               7e350b877a9a        3 years ago         317 MB
```
Based on that, it looks like MongoDB version 3.2.1

Method #2
You can open bash inside the MongoDB container and do a --version on mongodump
```
docker exec -it 4ceedframework_mongodb_1 /bin/bash
root@4519294b57c6:/# which mongodump
/usr/bin/mongodump
root@4519294b57c6:/# mongodump --version
mongodump version: 3.2.1
```
## MongoDB Bacup Script

Here is a handy backup script created by Gianni Pezzarosi and Phuong Nguyen to backup the MongDB database, compress it, and then email the status of it to someone.

```
#!/bin/bash

MONGO_DATABASE="clowder"
APP_NAME="4CeeD"

MONGO_HOST="127.0.0.1"
MONGO_PORT="27017"
TIMESTAMP=`date +%F-%H%M`
# The MONGODUMP_PATH is the path to the mongodump binary
MONGODUMP_PATH="/PATHTO/mongodb-3.4.17/bin/mongodump"
# The veriable BACKUPS_DIR is where the backups will be placed
BACKUPS_DIR="/PATHTO/mongodb_backups/$APP_NAME"
BACKUP_NAME="$APP_NAME-$TIMESTAMP"

echo "#################### $TIMESTAMP #####################"

$MONGODUMP_PATH -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE

# Create the backup directory
mkdir -p $BACKUPS_DIR
# rename dump to the variable $BACKUP_NAME defined above
mv dump $BACKUP_NAME
# Compress the backup
tar -zcvf $BACKUPS_DIR/$BACKUP_NAME.tgz $BACKUP_NAME
# Delete the original - uncompressed backup
rm -rf $BACKUP_NAME

# Email about the status of the backup
cat /var/log/4ceed-backup.log|tail -n 50|mail -s "[Backup Report] `hostname`" -a "/var/log/4ceed-backup.log" SOMEONESEMAILHERE
```
