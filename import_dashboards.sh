#!/bin/bash

# Start Kibana in background
/usr/local/bin/kibana-docker &

# Wait till kibana is online
while [[ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:5601/api/status)" != "200" ]]; do
  echo "Wait for Kibana"
  sleep 5
done

# Import Dashboard
echo "Import Dashboard"
curl -X POST http://localhost:5601/api/saved_objects/_import \
  -H "kbn-xsrf: true" \
  -H "Content-Type: multipart/form-data" \
  -F file=@/usr/share/kibana/config/export.ndjson

wait