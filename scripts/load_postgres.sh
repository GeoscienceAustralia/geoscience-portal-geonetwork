#!/bin/bash

pushd ~ubuntu/geonetwork


DB_PASSWORD=$( aws ssm get-parameters --name ausgin.catalog.db-password --region ap-southeast-2 --with-decryption --query Parameters[0].Value )

DB_PASSWORD=`echo $DB_PASSWORD | sed -e 's/^"//' -e 's/"$//'`

sed -i 's/__PASSWORD__/'"${DB_PASSWORD}"'/' src/main/webapp/WEB-INF/config-db/jdbc.properties

mvn clean package
