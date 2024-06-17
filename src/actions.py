from Db import Db
from tkinter import *
from Hash import Hasher


class Actions:
    def __init__(self):
        self.database = Db('../db/data.db')

    # TODO add a widget method that will be used to display messages to the user
    def widget(self, text: str = None, textbox: bool = False, cancel: bool = False, function: object() = None):
        width = len(text) * 10
        height = width
        widget = Tk(f"{width}x{height}", text)
        # if we have a textbox and cancel button and a function then we want user to input something
        if textbox and cancel and function is not None:
            entr = Entry(widget)
            entr.pack()
            Button(widget, text="Cancel", command=widget.destroy).pack()
            button = Button(widget, text="Ok")
            button.bind("<Button-1>", lambda event: function(entr.get()))
            button.pack()
        else:
            widget.title("Message")
            widget.resizable(False, False)
            Label(widget, text=text).pack()
            button = Button(widget, text="Ok", command=widget.destroy)
            button.pack()

    def register(self, credentials: dict):
        validated = self.__validate_data(credentials)
        if not validated:
            return
        email = self.__validate_email(credentials[["email"]])
        if not email:
            return
        password = self.__validate_password(credentials["password"])
        if not password:
            return
        credentials[2] = Hasher.hash_password(credentials["password"])
        self.database.create(*credentials)
        self.widget("User Created")

    def login(self, credentials: dict) -> list or None:
        validated = self.__validate_data(credentials)
        if not validated:
            return None
        credentials["password"] = Hasher.hash_password(credentials["password"])
        user = self.database.read(*credentials.values())
        if user:
            self.widget(f"Welcome {user[0][1]}")
            return user
        else:
            self.widget("Invalid Credentials")
            return None

    def delete_account(self, user: dict):
        self.database.delete(user["email"])
        self.widget("Account Deleted")
        user.clear()

    def change_password(self, user: dict):
        self.widget("Enter new password",True,True, self.change_password)
        if not self.__validate_password(new_password):
            return
        self.database.update(user["name"], user["surname"], Hasher.hash_password(new_password), user["email"])
        self.widget("Password Changed")

    def __validate_data(self, credentials: dict) -> bool:
        if "" in credentials.values():
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
