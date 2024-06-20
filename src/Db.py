import sqlite3
from User import User
from Exceptions import *


class Db:
    def __init__(self, db_name):
        self.db_name = db_name
        self._conn = sqlite3.connect(self.db_name)
        self.usr = User
        self._cursor = self._conn.cursor()

    def create(self, user: User) -> None:
        try:
            self._cursor.execute("INSERT INTO Users (name ,surname, password, Email) VALUES (?, ?, ?, ?)"
                                 , (user.name, user.surname, user.password, user.email))
            self._conn.commit()
        except sqlite3.IntegrityError:
            raise UserAlreadyExists("User already exists")

    def read(self, user: User) -> object | None:
        self._cursor.execute("SELECT * FROM Users where email = (?) and password = (?)",
                             (user.email, user.password))
        data = self._cursor.fetchall()
        if data:
            data = self.usr.from_db(data)
            return data
        return None

    def update(self, user: User) -> None:
        self._cursor.execute("Update users set name = (?), surname = (?), password = (?) where email = (?)",
                             (user.name, user.surname, user.password, user.email))
        self._conn.commit()

    def delete(self, user: User) -> None:
        self._cursor.execute('DELETE FROM users WHERE email = (?)', (user.email,))
        self._conn.commit()
