from Db import Db
from Hash import Hasher


class Actions:
    def __init__(self):
        self.__database = Db('../db/data.db')

    def register(self, credentials: dict):
        validated = self.__validate_data(credentials)
        if not validated:
            return False
        email = self.__validate_email(credentials["email"])
        if not email:
            return False
        password = self.__validate_password(credentials["password"])
        if not password:
            return False
        credentials["password"] = Hasher.hash_password(credentials["password"])
        self.__database.create(credentials)

    def login(self, credentials: dict) -> dict[str:str] | None:
        validated = self.__validate_data(credentials)
        if not validated:
            raise ValueError("Invalid data")
        credentials["password"] = Hasher.hash_password(credentials["password"])
        user = self.__database.read(*credentials.values())
        if user:
            return user
        else:
            raise ValueError("Invalid credentials")

    def delete_account(self, user: dict):
        self.__database.delete(user["email"])

    def change_password(self, user: dict):
        if not self.__validate_password(user["password"]):
            return False
        self.__database.update(user)
        return True

    def __validate_data(self, credentials: dict) -> bool:
        if "" in credentials.values():
            return False
        return True

    def __validate_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        return True

    def __validate_email(self, email: str) -> bool:
        if '@' not in email or '.' not in email:
            return False
        return True
