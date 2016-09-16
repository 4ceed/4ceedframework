# Install clowder server
FROM openjdk:7
MAINTAINER Phuong Nguyen <pvnguye2@illinois.edu>

# expose some properties of the container
EXPOSE 9000
ENV CLOWDER_CONTEXT="/" \
    CLOWDER_ADMINS="pvnguye2@illinois.edu" \
    MONGO_URI="mongodb://192.168.3.162:27017/clowder" \
    SMTP_HOST="express-smtp.cites.uiuc.edu" \
    RABBITMQ_EXCHANGE="clowder" \
    RABBITMQ_VHOST="%2F" \
    RABBITMQ_URI="amqp://guest:guest@192.168.3.153:5672/%2f" \
    RABBITMQ_MGMT_PORT="15672" \
    ELASTICSEARCH_SERVICE_CLUSTERNAME="myesdb" \
    ELASTICSEARCH_SERVICE_SERVER="192.168.3.2" \
    ELASTICSEARCH_SERVICE_PORT="9300" \
    TOOLMANAGER_URI=""

# copy the build file, this requires sbt dist to be run
COPY . /clowder

# change to user clowder
WORKDIR /clowder

# Compile clowder
RUN /clowder/sbt compile; exit 0

# command to run when starting docker
CMD ["/clowder/curator-start.sh"]
