#!/bin/bash

unzip -o src/main/resources/geonetwork-db.zip
psql -U postgres -f src/main/resources/geonetwork-db.sql

