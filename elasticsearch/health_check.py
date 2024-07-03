import json
import os

from elasticsearch import Elasticsearch


try:
    port_of_data_preparer = os.environ["ELASTICSEARCH_DATA_PREPARER_PORT"]
    es = Elasticsearch(
        hosts=[{"host": "host.docker.internal", "port": int(port_of_data_preparer), "scheme": "http"}]
        # basic_auth=("elastic", "MagicWord")
    )
    exit(0)
except Exception as ex:
    print(ex)
    exit(1)
