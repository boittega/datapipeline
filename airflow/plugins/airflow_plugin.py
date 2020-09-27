from airflow.plugins_manager import AirflowPlugin
from operators.twitter_operator import TwitterOperator
from operators.postgres_bulkload_operator import PostgresBulkLoadOperator


class AirflowPlugin(AirflowPlugin):
    name = "my_plugins"
    operators = [TwitterOperator, PostgresBulkLoadOperator]
