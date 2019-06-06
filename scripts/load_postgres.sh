#!/bin/bash

pushd ~ubuntu/geonetwork


echo $GEONETWORK_PASSWORD
sed -i 's/${password}/'"${GEONETWORK_PASSWORD}"'/' src/main/webapp/WEB-INF/config-db/jdbc.properties

mvn clean package
