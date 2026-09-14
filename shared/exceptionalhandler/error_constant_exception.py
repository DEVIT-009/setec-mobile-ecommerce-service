from enum import Enum

class ErrorConstantException(Enum):
    VALIDATION_ERROR = ("VALIDATION_ERROR", "Validation failed")
    UNKNOWN_ERROR = ("UNKNOWN_ERROR", "Unknown error")
    ERROR = ("ERROR", "Internal server error")

    def __init__(self, code, message):
        self.code = code
        self.message = message
