#!/bin/bash

# Import Dashboard
echo "Import Dashboard"
curl -X POST "http://localhost:${KIBANA_PORT}/api/saved_objects/_import" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: multipart/form-data" \
  -F file=@./export.ndjson

# wait
