import glob
from typing import Optional, List

from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults


class PostgresBulkLoadOperator(BaseOperator):
    """
    Executes sql code in a specific Postgres database

    :param table_name: Schema and table name
    :type table_name: str
    :param fields: List of table fields in the same order
    they appear in the file
    :type fields: List[str]
    :param folder: Folder containing CSV files to be copied
    :type folder: str
    """

    template_fields = ("folder",)
    ui_color = "#ededff"

    @apply_defaults
    def __init__(
        self,
        table_name: str,
        fields: List[str],
        folder: str,
        postgres_conn_id: str = "postgres_default",
        autocommit: Optional[bool] = False,
        database: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.table_name = table_name
        self.fields = fields
        self.folder = folder
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.database = database

    def execute(self, context):
        hook = PostgresHook(
            postgres_conn_id=self.postgres_conn_id, schema=self.database
        )
        sql = f"""
        COPY {self.table_name}({','.join(self.fields)})
        FROM STDIN WITH CSV HEADER
        """
        self.log.info(f"Executing: {sql}")
        for filename in glob.glob(self.folder):
            self.log.info(f"Copying file: {filename}")
            hook.copy_expert(sql=sql, filename=filename)
            for output in hook.conn.notices:
                self.log.info(output)
