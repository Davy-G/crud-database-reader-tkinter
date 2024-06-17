from tkinter import *
from actions import Actions


class Gui(Tk):
    def __init__(self, size: str = '600x600', title: str = "App"):
        super().__init__()
        self.geometry(size)
        self.resizable(False, False)
        self.cursor = Actions()
        self.user = None
        self.title(title)
        self.main_page()
        self.mainloop()

    def cls(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame = Frame(self)
        self.frame.pack()
# TODO add delete account and change password options
    def cabinet(self):
        self.cls()
        Label(self.frame, text=f'Welcome {self.user[0][1]}').pack()
        btn = Button(self.frame, text='Log Out', command=self.main_page)
        btn.bind('<Button-1>', lambda event: self.user.clear())
        btn.pack()
        Button(self.frame, text='Change My Password', command=self.cursor.change_password(user=self.user)).pack()
        Button(self.frame, text='Delete My Account', command=self.cursor.delete_account(user=self.user)).pack()


    def register_page(self):
        self.cls()
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
        password = Entry(self.frame, show="*")
        password.pack()
        button = Button(self.frame, text='Register')
        button.bind('<Button-1>', lambda event: self.cursor.register({"name": name.get(), "surname": surname.get(),
                                                                      "email": email.get(), "password": password.get()}))
        button = Button(self.frame, text='Back to login page', command=self.main_page)
        button.pack()

    def main_page(self):
        self.cls()
        Label(self.frame, text='Log In').pack(pady=50)
        Label(self.frame, text='Email').pack()
        email = Entry(self.frame)
        email.pack()
        Label(self.frame, text='Password').pack()
        password = Entry(self.frame, show="*")
        password.pack()
        button = Button(self.frame, text='Log In')
        button.bind('<Button-1>', lambda event: self.__handle_login({"email": email.get(), "password": password.get()}))
        button.pack()
        Label(self.frame, text='Dont have an account?').pack()
        Button(self.frame, text='Register', command=self.register_page).pack()

    def __handle_login(self, credentials: dict):
        self.user = self.cursor.login(credentials)
        self.cabinet() if self.user is not None else self.main_page()

