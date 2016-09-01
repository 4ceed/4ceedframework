#!/bin/bash

# Some helper functions

# add/replace plugin if variable is non empty
# $1 = variable to check if defined
# $2 = index of plugin
# $3 = plugin class
function fix_plugin() {
    if [ "$2" == "" ]; then return 0; fi
    if [ "$3" == "" ]; then return 0; fi

    if [ -e /clowder/custom/play.plugins ]; then
        mv /clowder/custom/play.plugins /clowder/custom/play.plugins.old
        grep -v ":$2" /clowder/custom/play.plugins.old > /clowder/custom/play.plugins
        rm /clowder/custom/play.plugins.old
    fi
    if [ "$1" != "" ]; then
        echo "$2:$3" >> /clowder/custom/play.plugins
    fi
}

# add/replace if variable is non empty
# $1 = variable to replace/remove
# $2 = new value to set
# $3 = additional variable to remove
function fix_conf() {
    local query
    if [ "$1" == "" ]; then return 0; fi

    if [ -e /clowder/custom/custom.conf ]; then
        if [ "$3" == "" ]; then
            query="$1"
        else
            query="$1|$3"
        fi

        mv /clowder/custom/custom.conf /clowder/custom/custom.conf.old
        grep -v "^(${query})=" /clowder/custom/custom.conf.old > /clowder/custom/custom.conf
        rm /clowder/custom/custom.conf.old
    fi

    if [ "$2" != "" ]; then
        echo "$1=\"$2\"" >> /clowder/custom/custom.conf
    fi
}

# Update configurations
# admins
if [ "$CLOWDER_ADMINS" == "" ]; then
fix_conf   "registerThroughAdmins" "false"
fix_conf   "initialAdmins" ""
else
fix_conf   "registerThroughAdmins" "true"
fix_conf   "initialAdmins" "$CLOWDER_ADMINS"
fi

# rabbitmq
fix_plugin "$RABBITMQ_URI" "9992" "services.RabbitmqPlugin"
fix_conf   "clowder.rabbitmq.uri" "$RABBITMQ_URI" "medici2.rabbitmq.uri"
fix_conf   "clowder.rabbitmq.exchange" "$RABBITMQ_EXCHANGE" "medici2.rabbitmq.exchange"
fix_conf   "clowder.rabbitmq.managmentPort" "$RABBITMQ_MGMT_PORT" "medici2.rabbitmq.managmentPort"

# mongo
fix_conf   "mongodbURI" "$MONGO_URI"

# smtp
fix_conf   "smtp.host" "$SMTP_HOST"
if [ "$SMTP_HOST" == "" ]; then
fix_conf   "smtp.mock" "true"
else
fix_conf   "smtp.mock" "false"
fi

# elasticsearch
fix_plugin "$ELASTICSEARCH_SERVICE_SERVER" "10700" "services.ElasticsearchPlugin"
fix_conf   "elasticsearchSettings.clusterName" "$ELASTICSEARCH_SERVICE_CLUSTERNAME"
fix_conf   "elasticsearchSettings.serverAddress" "$ELASTICSEARCH_SERVICE_SERVER"
fix_conf   "elasticsearchSettings.serverPort" "$ELASTICSEARCH_SERVICE_PORT"

# toolmanager
fix_plugin "$TOOLMANAGER_URI" "11000" "services.ToolManagerPlugin"
fix_conf   "toolmanagerURI" "$TOOLMANAGER_URI"

# Start clowder
cd /clowder
screen -d -m ./sbt run
tail -f /dev/null
