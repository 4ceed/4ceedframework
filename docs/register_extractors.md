How to: Register Extractors in Kubernetes
====

To register extractors to 4CeeD framework, you first need to have a 4CeeD instance running and create an 
account for the administrator. Please make sure that the information in `custom.conf` file are correct and 
present newly deployed 4CeeD instance (especially `ADMIN_EMAIL` and `CURATOR_ADDR` information).

After that, you can register all supported extractors and make them available for 4CeeD users by running the 
following script:

```
./register_extractors.sh
```

You will be asked to enter username and password to register the extractors. Please use the administrator's 
username and password.

After registering the extractors, you can test them by uploading sample files (located in `samples/`) to 4CeeD.

