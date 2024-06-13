"""
This ecnoder supports JSON encoding of Decimal
"""
from datetime import datetime
from decimal import Decimal
from json import JSONEncoder


class DecimalEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return o.__dict__