import uuid
import re
import random

class Guid:
    prefix = 'A_'
    ext = '[^-]{8}'

    @classmethod
    def get_order_number(cls):
        guid = str(uuid.uuid4())
        match = re.search(cls.ext, guid)
        return str(cls.prefix + match[0])

    @classmethod
    def get_random_number(cls):
        uid = str(random.randint(100000, 999999))
        return str(cls.prefix + uid)
