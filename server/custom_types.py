from enum import Enum


class MessageType(str, Enum):
    READY = "READY"
    ERROR = "ERROR"
    UPDATE = "UPDATE"
