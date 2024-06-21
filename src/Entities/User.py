from dataclasses import dataclass


@dataclass
class User:
    id: int = None
    name: str = None
    surname: str = None
    email: str = None
    password: str = None

    @property
    def data(self) -> list[str]:
        return [self.name, self.surname, self.password, self.email]

    @classmethod
    def from_db(cls, db_params: list) -> object:
        return cls(*db_params[0])

    def reset(self):
        self.id = None
        self.name = None
        self.surname = None
        self.password = None
        self.email = None

    def strip(self):
        self.name = self.name.strip()
        self.surname = self.surname.strip()
        self.email = self.email.strip()
        self.password = self.password.strip()

# class UserSession(User):
#     def __init__(self, user: object):
#         super().__init__()
#         self.__user = None
#
#     def get_user(self) -> str:
#         return self.__user.name
#
#     def reset(self):
#         self.__user = None
