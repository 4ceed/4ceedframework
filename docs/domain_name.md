How to: Access 4CeeD through Domain Name
====

## DNS setup

Please note this document was written for 4ceed running on a CentOS 7 machine. Your package manager and configuration files may be different based on the OS you are running.

To access 4CeeD curator via a domain name, you first need to setup DNS mapping between your domain name (e.g., http://4ceed.example.com) and the IP address of the host where 4CeeD curator can be accessed. Such a mapping often can be done via your organization's IT department (in case the domain name is only accessible in your organization's intranet) or via DNS service provider (e.g., where you register your domain, in case 4CeeD service is accessible through the Internet).

## Setup access to 4CeeD via port 80 (HTTP)

By default, 4CeeD curation service can be accessible via `http://[HOST_IP]:9000` (or `http://[DOMAIN_NAME]:9000`, in case domain name is setup). If you want to provide access via port 80 (i.e., `http://[HOST_IP]`, or `http://[DOMAIN_NAME]`), you can setup an [NGINX](https://www.nginx.com/) server on the host server to redirect traffic from port 32500 to port 80.

First Install Nginx via yum:
`yum install nginx -y`

Replace the default `server` block in  `/etc/nginx/nginx.conf`:
```
    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
``` 
With this one:

```
server {                                                                               
    listen 80;                                                                         
    client_max_body_size 1000M;  # Configure maximum upload filesize                   
    location / {                                                                       
        if ($request_method = POST) {                                                  
            return 307 http://$host$request_uri;                                      
        }                                                                              
        return 301 http://$host:9000$request_uri;                                    
    }                                                                                  
}
```

## Setup access to 4CeeD via HTTPS (port 443) 

To provide encryption for the communication between 4CeeD client and curator service, we suggest users to enable HTTPS access to 4CeeD curator. Before setting up HTTPS access, you first need to acquire a certificate (e.g., `/etc/nginx/ssl/4ceed.crt`) and a private key (e.g., `/etc/nginx/ssl/4ceed.key`) for your 4CeeD curator server. 

Then, you can configure NGINX to accept HTTPS connections and redirect all traffic from HTTP port 80 to HTTPS port 443 (`HOST_IP` is the IP address of the host where 4CeeD is accessible):

```
server {
    listen 80;
    client_max_body_size 1000M; # Configure maximum upload filesize
    location / {
        if ($request_method = POST) {
            return 307 https://$host$request_uri;
        }
        return 301 https://$host:9000$request_uri;
    }
}

server {
    listen 443 ssl;
    port_in_redirect off;
    ssl_certificate /etc/nginx/ssl/4ceed.crt;
    ssl_certificate_key /etc/nginx/ssl/4ceed.key;
    client_max_body_size 1000M;

    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
    location / {
        proxy_http_version 1.1;
        proxy_pass http://[HOST_IP]:9000;
    }

}
```
Then start nginx:
`systemctl start nginx`
Then enable nginx:
`systemctl enable nginx`
