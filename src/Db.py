import sqlite3


class Db:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create(self, name: str, surname: str, pasword: str, email: str):
        query = "INSERT INTO Users (name ,surname, password, Email) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, surname, pasword, email))
        self.conn.commit()

    def read(self, email: str, password: str):
        self.cursor.execute("SELECT * FROM Users where Email = (?) and Password = (?)", (email, password))
        return self.cursor.fetchall()

    def update(self, name: str, surname: str, pasword: str, email: str):
        self.cursor.execute("Update users set name = (?), surname = (?), password = (?) where Email = (?)",
                            (name, surname, pasword, email))
        self.conn.commit()
        return self.cursor.fetchall()

    def delete(self, email: str):
        self.cursor.execute('DELETE FROM users WHERE Email = (?)', (email,))
        self.conn.commit()
