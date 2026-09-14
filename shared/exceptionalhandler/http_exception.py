from rest_framework.exceptions import APIException

class HttpException(APIException):
    def __init__(self, message, status_code, error):
        self.status_code = status_code
        self.error = error
        super().__init__(message)
