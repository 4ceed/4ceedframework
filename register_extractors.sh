#!/bin/bash

# Setup environment variables
source custom.conf

if [ "$1" != "" ] ; then
	extractor_info=$(cat $1)
	curl -k -X POST \
		-H "Content-Type: application/json" \
		-d "${extractor_info}" \
		-u $ADMIN_EMAIL \
		"${CURATOR_ADDR}/api/extractors"
else
	# Register extractors in 'extractors/' dir
	for extractor_file in $(find extractors/ -name '*.json'); do
	    echo "Register extractor ${extractor_file}..."
	    extractor_info=$(cat $extractor_file)
	    curl -k -X POST \
		-H "Content-Type: application/json" \
		-d "${extractor_info}" \
		-u $ADMIN_EMAIL \
		"${CURATOR_ADDR}/api/extractors"
	done
fi

