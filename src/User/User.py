from dataclasses import dataclass


@dataclass
class User:
    name: str
    surname: str
    email: str
    password: str

    @property
    def to_db(self) -> list[str]:
        return [self.name, self.surname, self.password, self.email]

    @classmethod
    def from_db(cls, db_params: list[str, str, str, str]):
        return cls(*db_params)
