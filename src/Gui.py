from tkinter import *
from tkinter import ttk
from src.Db import Db


class Gui(Tk):
    def __init__(self, size: str = '600x600', title: str = "App"):
        super().__init__()
        self.geometry(size)
        self.resizable(False, False)
        self.title(title)
        self.frame = ttk.Frame(self)
        self.database = Db('../db/data.db')

    def __widget(self, size: str = "200x200", text: str = None):
        widget = Gui(size, text)
        Label(widget, text=text,wraplength=450,anchor="center").pack()
        button = Button(widget, text="Ok", command=widget.destroy)
        button.pack()

    def cls(self):
        for widget in self.winfo_children():
            widget.destroy()

    def register_page(self):
        self.frame.pack()
        Label(self.frame, text='Register').pack(pady=50)
        Label(self.frame, text='Name').pack()
        name = Entry(self.frame)
        name.pack()
        Label(self.frame, text='Surname').pack()
        surname = Entry(self.frame)
        surname.pack()
        Label(self.frame, text='Email').pack()
        email = Entry(self.frame)
        email.pack()
        Label(self.frame, text='Password').pack()
        password = Entry(self.frame)
        password.pack()
        button = Button(self.frame, text='Register')
        button.bind('<Button-1>', lambda event: self.__register(name, surname, email, password))
        button.pack()
        self.mainloop()
    def main_page(self):
        self.frame.pack()
        Label(self.frame, text='Log In').pack(pady=50)
        Label(self.frame, text='Email').pack()
        email = Entry(self.frame)
        email.pack()
        Label(self.frame, text='Password').pack()
        password = Entry(self.frame)
        password.pack()
        button = Button(self.frame, text='Log In')
        button.bind('<Button-1>', lambda event: self.__login(email, password))
        button.pack()
        Label(self.frame, text='Dont have an account?').pack()
        register = Button(self.frame, text='Register', command=self.register_page)
        register.bind('<Button-1>', lambda event: self.cls())
        register.pack()
        self.mainloop()

    def __register(self, name: ttk.Entry, surname: ttk.Entry, email: ttk.Entry, password: ttk.Entry):
        credentials = name.get(), surname.get(), email.get(), password.get()
        self.database.create(*credentials)
        self.__widget("150x150", "User Created")

    def __login(self, email: ttk.Entry, password: ttk.Entry):
        credentials = email.get(), password.get()
        user = self.database.read(*credentials)
        if user:
            return user
        else:
            self.__widget("150x150", "Invalid Credentials")



