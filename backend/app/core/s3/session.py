import os

from aioboto3 import Session


class AWSSession(Session):
    """Class session to AWS."""
    def __new__(cls):
        """Method implement singleton pattern."""
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(
            self,
            aws_access_key_id=os.getenv("AWS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_KEY"),
            **kwargs
    ):
        super().__init__(aws_access_key_id, aws_secret_access_key, **kwargs)
