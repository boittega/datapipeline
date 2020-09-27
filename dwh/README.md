# Postgresql Datawarehouse

This folder contains Postgresql configuration to create a Datawarehouse for 
Twitter pipeline

# Makefile

The following tasks are available on make:

* build: Build Docker Postgresql image and volume
* start: Start Docker DWH container and create necessary tables and schemas
* stop: Stop Docker DWH container
* delete: Drop Docker volume deleting the database
