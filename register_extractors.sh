#!/bin/bash

# Setup environment variables
source custom.conf

# Register extractors in 'extractors/' dir
for extractor_file in $(find extractors/ -name '*.json'); do
    echo "Register extractor ${extractor_file}..."
    extractor_info=$(cat $extractor_file)
    curl -X POST \
        -H "Content-Type: application/json" \
        -d "${extractor_info}" \
        -u $ADMIN_EMAIL \
        "http://${CURATOR_IP}:32500/api/extractors"
done
