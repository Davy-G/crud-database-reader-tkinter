from src.dbo.Db import Db
from src.Utilities.Hash import Hasher
from src.Entities.User import User
from src.Utilities.Exceptions import *


class Actions:
    def __init__(self):
        self.__database = Db('../db/data.db')

    def register(self, credentials: User):
        if not self.__validate_data(credentials):
            raise ValidationError("Please fill all fields")

        if not self.__validate_email(credentials):
            raise InvalidEmail("Invalid email")

        if not self.__validate_password(credentials):
            raise InvalidPassword("Invalid password")
        credentials.password = Hasher.hash_password(credentials.password)
        self.__database.create(credentials)

    def login(self, credentials: User) -> dict[str:str] | bool:
        validated = self.__validate_data(credentials)
        if validated:
            credentials.password = Hasher.hash_password(credentials.password)
            user = self.__database.read(credentials)
            if user is not None:
                return user
            raise UserDoesNotExist("Invalid credentials")

        raise ValidationError("Please fill all fields")

    def get_products(self):
        return self.__database.get_products()

    def delete_account(self, user: User) -> None:
        self.__database.delete(user)

    def change_password(self, user: User, new_password: str) -> None:
        user.password = new_password
        if self.__validate_password(user):
            user.password = Hasher.hash_password(user.password)
            self.__database.update(user)
            return
        raise InvalidPassword("Invalid password")

    def __validate_data(self, credentials: User) -> bool:
        if "" or " " in credentials.data:
            return False
        return True

    def __validate_password(self, credentials: User) -> bool:
        if len(credentials.password) < 8:
            return False
        if not any(char.isdigit() for char in credentials.password):
            return False
        return True

    def __validate_email(self, credentials: User) -> bool:
        if '@' not in credentials.email or '.' not in credentials.email:
            return False
        return True
