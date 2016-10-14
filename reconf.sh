#!/bin/bash
source custom.conf

echo 'Reconfig Elasticsearch...'
sed -e "s/\\\$ELASTICSEARCH_IP/${ELASTICSEARCH_IP}/g;" \
    "tools/elasticsearch/es-svc.yaml.sed" > tools/elasticsearch/es-svc.yaml

echo 'Reconfig MongoDB...'
sed -e "s/\\\$MONGODB_IP/${MONGODB_IP}/g;" \
    "tools/mongodb/mongo-service.yaml.sed" > tools/mongodb/mongo-service.yaml

echo 'Reconfig RabbitMQ...'
sed -e "s/\\\$RABBITMQ_IP/${RABBITMQ_IP}/g;" \
    "tools/rabbitmq/rabbitmq-service.yaml.sed" > tools/rabbitmq/rabbitmq-service.yaml

echo 'Reconfig Curator...'
sed -e "s/\\\$ELASTICSEARCH_IP/${ELASTICSEARCH_IP}/g;"`
    `"s/\\\$MONGODB_IP/${MONGODB_IP}/g;"`
    `"s/\\\$UPLOADER_IP/${UPLOADER_IP}/g;"`
    `"s/\\\$RABBITMQ_IP/${RABBITMQ_IP}/g;"`
    `"s/\\\$ADMIN_EMAIL/${ADMIN_EMAIL}/g;"`
    `"s/\\\$SMTP_SERVER/${SMTP_SERVER}/g;" \
    "curator/curator-rc.yaml.sed" > curator/curator-rc.yaml

echo 'Reconfig Uploader...'
sed -e "s/\\\$CURATOR_IP/${CURATOR_IP}/g;"`
    `"s/\\\$UPLOADER_IP/${UPLOADER_IP}/g;" \
    "uploader/uploader-rc.yaml.sed" > uploader/uploader-rc.yaml

echo 'Reconfig extractors...'
sed -e "s/\\\$RABBITMQ_IP/${RABBITMQ_IP}/g;" \
    "extractors/dm3-extractor.yaml.sed" > extractors/dm3-extractor.yaml
sed -e "s/\\\$RABBITMQ_IP/${RABBITMQ_IP}/g;"`
    `"s/\\\$CURATOR_IP/${CURATOR_IP}/g;" \
    "extractors/sem-extractor.yaml.sed" > extractors/sem-extractor.yaml
sed -e "s/\\\$RABBITMQ_IP/${RABBITMQ_IP}/g;" \
    "extractors/xray-extractor.yaml.sed" > extractors/xray-extractor.yaml
sed -e "s/\\\$RABBITMQ_IP/${RABBITMQ_IP}/g;" \
    "extractors/image-preview-extractor.yaml.sed" > extractors/image-preview-extractor.yaml
sed -e "s/\\\$RABBITMQ_IP/${RABBITMQ_IP}/g;" \
    "extractors/afm-extractor.yaml.sed" > extractors/afm-extractor.yaml
