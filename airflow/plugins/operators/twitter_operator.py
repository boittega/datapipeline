from airflow.utils.decorators import apply_defaults
from hooks.twitter_hook import TwitterHook
from airflow.models import BaseOperator


class TwitterOperator(BaseOperator):
    """
    """

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.hook = TwitterHook()
