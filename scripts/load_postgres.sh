#!/bin/bash

pushd ~ubuntu/geonetwork

unzip src/main/resources/geonetwork-db.zip
export GEONETWORK_PASSWORD=`date | sha512sum | base64 | head -c 32` &> /dev/null
echo $GEONETWORK_PASSWORD
sed -i 's/${password}/'"${GEONETWORK_PASSWORD}"'/' src/main/resources/geonetwork-db.sql
sudo psql -U postgres -f src/main/resources/geonetwork-db.sql


echo $GEONETWORK_PASSWORD
sed -i 's/${password}/'"${GEONETWORK_PASSWORD}"'/' src/main/webapp/WEB-INF/config-db/jdbc.properties

mvn clean package
