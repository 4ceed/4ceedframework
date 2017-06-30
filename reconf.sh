#!/bin/bash
source custom.conf

echo 'Reconfigure 4CeeD...'
sed -e "s/\\\$ADMIN_EMAIL/${ADMIN_EMAIL}/g;"`
    `"s/\\\$SMTP_SERVER/${SMTP_SERVER}/g;"`
    `"s/\\\$VERSION/${VERSION}/g;" \
    "curator/curator-rc.yaml.sed" > curator/curator-rc.yaml

sed -e "s~\\\$CURATOR_ADDR~${CURATOR_ADDR}~g;" \
    "extractors/sem-extractor.yaml.sed" > extractors/sem-extractor.yaml
sed -e "s~\\\$CURATOR_ADDR~${CURATOR_ADDR}~g;" \
    "extractors/zip-extractor.yaml.sed" > extractors/zip-extractor.yaml
