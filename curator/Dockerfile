# Install curator server
FROM openjdk:7
MAINTAINER Phuong Nguyen <pvnguye2@illinois.edu>

# expose some properties of the container
EXPOSE 9000

# copy the build file, this requires sbt dist to be run
COPY . /clowder

# change to user clowder
WORKDIR /clowder

# Compile clowder
RUN /clowder/sbt compile; exit 0

# command to run when starting docker
CMD ["/clowder/curator-start.sh"]
