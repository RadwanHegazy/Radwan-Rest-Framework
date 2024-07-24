
class ValidationError (BaseException) :
    def __init__(self, message,*args: object) -> None:
        self.message = message
        super().__init__(message,*args) 