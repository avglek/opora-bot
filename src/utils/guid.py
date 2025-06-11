import uuid
import re

class Guid:
    prefix = 'A_'
    ext = '[^-]{8}'

    @classmethod
    def get_order_number(cls):
        guid = str(uuid.uuid4())
        match = re.search(cls.ext, guid)
        return str(cls.prefix + match[0])
