class UserDoesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidPassword(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidEmail(Exception):
    def __init__(self, message):
        super().__init__(message)


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidPasswordFormat(Exception):
    def __init__(self, message):
        super().__init__(message)
