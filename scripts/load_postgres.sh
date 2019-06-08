#!/bin/bash

pushd ~ubuntu/geonetwork

# Get RDS password from key store and rewrite JDBC config
DB_PASSWORD=$( aws ssm get-parameters --name ausgin.catalog.db-password --region ap-southeast-2 --with-decryption --query Parameters[0].Value )
DB_PASSWORD=`echo $DB_PASSWORD | sed -e 's/^"//' -e 's/"$//'`
sed -i 's/__PASSWORD__/'"${DB_PASSWORD}"'/' src/main/webapp/WEB-INF/config-db/jdbc.properties


# Install GeoNetwork WAR
mvn clean package
sudo rm -rf /var/lib/tomcat8/webapps/geonetwork*
sudo mv target/geonetwork.war /var/lib/tomcat8/webapps/