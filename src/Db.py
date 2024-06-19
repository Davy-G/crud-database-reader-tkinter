import sqlite3
import User.User as User


class Db:
    def __init__(self, db_name):
        self.db_name = db_name
        self._conn = sqlite3.connect(self.db_name)
        self.usr = User.User
        self._cursor = self._conn.cursor()

    def create(self, user: dict) -> None:
        self._cursor.execute("INSERT INTO Users (name ,surname, password, Email) VALUES (?, ?, ?, ?)"
                             , (user["name"], user["surname"], user["password"], user["email"]))
        self._conn.commit()

    def read(self, email: str, password: str) -> dict:
        self._cursor.execute("SELECT * FROM Users where email = (?) and password = (?)",
                             (email, password))
        user = self._cursor.fetchall()
        if user:
            return self.usr.from_db(user)
        return {}

    def update(self, user: dict) -> None:
        self._cursor.execute("Update users set name = (?), surname = (?), password = (?) where email = (?)",
                             (user["name"], user["surname"], user["password"], user["email"]))
        self._conn.commit()

    def delete(self, email: str) -> None:
        self._cursor.execute('DELETE FROM users WHERE email = (?)', (email,))
        self._conn.commit()
