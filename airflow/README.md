# Airflow local folder

This folder contains Airflow DAG, Operator and Hook used to extract Twitter data.

# Makefile

The following tasks are available on make:

* install: Install Airflow version 1.10.12 and start Airflow DB
* start: Set project enviroment variables and start Airflow scheduler and webserver
* stop: Kill Airflow scheduler and webserver processes
