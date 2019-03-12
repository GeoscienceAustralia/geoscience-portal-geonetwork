#!/bin/bash

SQL_FILE=src/main/resources/geonetwork-db.sql

pg_dump -U geonetwork -c -C  > $SQL_FILE
patch $SQL_FILE < src/main/resources/deploy.patch
zip src/main/resources/geonetwork-db.zip $SQL_FILE
