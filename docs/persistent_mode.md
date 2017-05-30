Run 4CeeD in Persistent Mode
====

With the default setting of 4CeeD, data is stored in a non-persistent mode (i.e., when the Kubernetes instance is taken down, the data is deleted). To enable the persistent mode, you can do the following steps:

## Update database configs
- To enable persistent mode for MongoDB, you first just need to edit file `tools/mongodb/mongodb-rc.yaml`, and change the `name` in:
```
volumeMounts:
- name: temporary-storage
  mountPath: "/data/db"
```

to `persistent-storage`:

```
volumeMounts:
- name: persistent-storage
  mountPath: "/data/db"
```

- Next, in the same file, you can update the `path` variable in:

```
- name: persistent-storage
  hostPath:
	path: "/mnt/nfs/mongodb"
```

to any path on your system that you want to store data persistently. 

## Update search service configs 

To enable the persistent mode for Elasticsearch, you can follow the same steps as for MongoDB, this time, the file to edit is `tools/elasticsearch/elasticsearch-rc.yaml`
