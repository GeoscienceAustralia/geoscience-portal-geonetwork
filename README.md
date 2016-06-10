#Getting started with your local instance of GeoNetwork

##Setting up Postgres

Make sure you have postgres installed and configured correctly.

Edit the src/main/resources/geonetwork-db.sql and replace the variable ${password} with your own dummy password (eg 'test').

Execute the command:

    psql -U postgres -f src/main/resources/geonetwork-db.sql

This will build the database that conatins the metadata records for you GeoNetwork instance.

##Building the GeoNetwork instance

Edit `src/main/webapp/WEB-INF/config-db/jdbc.properties`, replace the variable `${password}` with the dummy password you used for the SQL.

Run `mvn install` then deploy the warfile to your local Tomcat container.

##Making changes to the GeoNetwork configuration

Most changes are made in the GeoNetwork web interface and these changes are persisted in the postgres database. To deploy these changes, we need to dump the database. 

    pg_dump -U geonetwork -c -C  > src/main/resources/geonetwork-db.sql

This will not create the `geonetwork` user required for deployment. It is added by the following command.

    patch src/main/resources/geonetwork-db.sql < src/main/resources/deploy.patch

##Troubleshooting

If you are getting locale or encoding errors for you local Postgres database, edit the line that creates the `geonetwork` database. But ensure that when you commit the geonetwork.-db.sql file your `CREATE DATABASE` statement matches:

    CREATE DATABASE geonetwork WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C' LC_CTYPE = 'C';

Otherwise it will not work on our EC2 instance.
