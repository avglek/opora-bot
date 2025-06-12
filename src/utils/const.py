import enum

class Status(enum.Enum):
    NEW = 1
    PENDING = 2
    IN_PROGRESS = 3
    COMPLETED = 4