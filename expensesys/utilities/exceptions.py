class ApplicationError(Exception):
    def __init__(self, message="There was an error", extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}
