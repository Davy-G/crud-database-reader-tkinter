from Db import Db
from tkinter import Label, Button, Tk
from Hash import Hasher


class Actions:
    def __init__(self):
        self.database = Db('../db/data.db')



    def widget(self, text: str = None):
        width = len(text) * 10
        height = width // 2
        widget = Tk(f"{width}x{height}", text)
        widget.title("Message")
        widget.resizable(False, False)
        Label(widget, text=text).pack()
        button = Button(widget, text="Ok", command=widget.destroy)
        button.pack()

    def register(self, credentials: list):
        validated = self.__validate_data(credentials)
        if not validated:
            return
        email = self.__validate_email(credentials[3])
        if not email:
            return
        password = self.__validate_password(credentials[2])
        if not password:
            return
        credentials[2] = Hasher.hash_password(credentials[2])
        self.database.create(*credentials)
        self.widget("User Created")

    def login(self, credentials: list):
        validated = self.__validate_data(credentials)
        if not validated:
            return None
        credentials[1] = Hasher.hash_password(credentials[1])
        user = self.database.read(*credentials)
        if user:
            self.widget(f"Welcome {user[0][1]}")
            return user
        else:
            self.widget("Invalid Credentials")
            return None

    def __validate_data(self, credentials: list) -> bool:
        if "" in credentials:
            self.widget("none of the fields can be empty")
            return False
        return True

    def __validate_password(self, password: str) -> bool:
        if len(password) < 8:
            self.widget("Password must be at least 8 characters long")
            return False
        if not any(char.isdigit() for char in password):
            self.widget("Password must contain at least one digit")
            return False
        return True

    def __validate_email(self, email: str) -> bool:
        if '@' not in email or '.' not in email:
            self.widget("Invalid Email")
            return False
        return True
