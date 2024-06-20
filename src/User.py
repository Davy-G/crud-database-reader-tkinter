from dataclasses import dataclass


@dataclass
class User:
    name: str = None
    surname: str = None
    email: str = None
    password: str = None

    @property
    def data(self) -> list[str]:
        return [self.name, self.surname, self.password, self.email]


    @classmethod
    def from_db(cls, db_params: list[str]) -> object:
        return cls(*db_params)

    def reset(self):
        self.name = None
        self.surname = None
        self.password = None
        self.email = None
