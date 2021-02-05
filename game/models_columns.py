import json
import sqlalchemy
from datetime import date, time, datetime, timedelta
from sqlalchemy.types import TypeDecorator

SIZE = 256

default = lambda obj: obj.__str__() if isinstance(obj, (date, time, datetime, timedelta)) else obj

class TextPickleType(TypeDecorator):

    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, default=default)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value