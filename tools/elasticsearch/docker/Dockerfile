FROM quay.io/pires/docker-elasticsearch:1.7.2

MAINTAINER pjpires@gmail.com

# Override elasticsearch.yml config, otherwise plug-in install will fail
ADD do_not_use.yml /elasticsearch/config/elasticsearch.yml

# Install Elasticsearch plug-ins
RUN /elasticsearch/bin/plugin install io.fabric8/elasticsearch-cloud-kubernetes/1.3.0 --verbose

# Install Marvel
RUN /elasticsearch/bin/plugin install elasticsearch/marvel/latest --verbose

RUN /elasticsearch/bin/plugin install mobz/elasticsearch-head

# Override elasticsearch.yml config, otherwise plug-in install will fail
ADD elasticsearch.yml /elasticsearch/config/elasticsearch.yml

# Copy run script
COPY run.sh /
