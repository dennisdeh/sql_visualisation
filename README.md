# Simple SQL Visualisation
## Introduction
Simple containerised application based on steamlit to visualise data in an SQL database. The app is configured with a database running in a MariaDB container, with an administration interface container. Some dummy data in two tables in the 'default' database have been added to make the app self-contained. If a database running on the host or in a different container on the same virtual network should be used, some simple changes in the docker-compose.yml and .env file must be made (see below).

## Instructions
 - Specify SQL configuration and database in the .env file.
 - Specify login details, ports etc. in the .env file
 - If another database located on the host should be used, the environment variables DB_HOST and DB_PORT needs to be changed in the docker-compose.yml file.