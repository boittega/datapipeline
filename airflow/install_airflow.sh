
pip install psycopg2-binary

pip install apache-airflow[postgresql]==1.10.12 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"

airflow initdb
