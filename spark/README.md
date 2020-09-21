# Twitter transformation Spark job

This folder contains the Spark job used to transform the twitter data from raw 
into the data lake format.
This job will extract tweet and user data, flatten the data structure and export 
into Parquet file format.

# Makefile

The following tasks are available on make:

* install: Download Spark
* test: Test Spark job
* run: Manually run, with parameters:
    * --src: Source folder or file
    * --dest: Destination folder
