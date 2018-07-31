#!/bin/bash

cp ~ubuntu/geonetwork/target/geonetwork.war /var/lib/tomcat8/webapps
service tomcat8 start
