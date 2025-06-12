# How to run elasticserach via docker

docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.4

-- to check that it is running:
curl http://localhost:9200

It will return JSON 
{
  "name" : "3e427f1a5ae5",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "qq4g0XBPQQuAjjCP4t6FUg",
  "version" : {
    "number" : "8.13.4",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "da95df118650b55a500dcc181889ac35c6d8da7c",
    "build_date" : "2024-05-06T22:04:45.107454559Z",
    "build_snapshot" : false,
    "lucene_version" : "9.10.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}

-- to remove existed docker:
docker rm -f elasticsearch
