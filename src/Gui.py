from customtkinter import *
from actions import Actions
from User.User import User
from PIL import Image


class App(CTk):
    def __init__(self, grid="1000x500", **kwargs):
        super().__init__(**kwargs)
        self.geometry(grid)
        self.__cursor = Actions()
        self._user = {}

        container = CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, RegistrationPage, Cabinet):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def __widget(self, text: str = None, textbox: bool = False, cancel: bool = False, function: callable = None):
        width = len(text) * 10
        height = width
        widget = CTkToplevel(self)
        widget.geometry(f"{width}x{height}")
        widget.title("Message")
        widget.resizable(False, False)

        if textbox and cancel and function is not None:
            entr = CTkEntry(widget)
            entr.pack()
            CTkButton(widget, text="Cancel", command=widget.destroy).pack()
            button = CTkButton(widget, text="Ok")
            button.bind("<Button-1>", lambda event: function(entr.get()))
            button.pack()
        else:
            CTkLabel(widget, text=text).pack()
            button = CTkButton(widget, text="Ok", command=widget.destroy)
            button.pack()

    def __cls(self):
        for widget in self.winfo_children():
            widget.destroy()

    def __handle_login(self, credentials: dict):
        self._user = self.__cursor.login(credentials)
        self.show_frame(Cabinet) if self._user is not None else self.show_frame(StartPage)

    def __handle_reg(self, credentials: dict):
        self._user = self.__cursor.register(credentials)


class StartPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = CTkFrame(self, width=400, height=500)
        CTkLabel(frame, text='Log In').pack(side="top", pady=50)
        CTkLabel(frame, text='Email').pack(side="top", pady=10)

        email = CTkEntry(frame, width=300)
        email.pack(side="top")

        CTkLabel(frame, text='Password').pack(side="top")

        password = CTkEntry(frame, show="*", width=300)
        password.pack(side="top", pady=10)

        button = CTkButton(frame, text='Log In')
        button.bind('<Button-1>',
                    lambda event: controller.__handle_login({"email": email.get(), "password": password.get()}))
        button.pack(side="top", pady=20)

        CTkLabel(frame, text="Don't have an account?").pack(pady=2)


        reg = CTkButton(frame, text='Register', command=lambda: controller.show_frame(RegistrationPage))
        reg.pack()

        frame.pack_propagate(False)
        frame.pack(side="right")

        frame2 = CTkFrame(self, width=600, height=500, border_color="red", border_width=1)
        image = Image.open("Style/images/textile.jpg")
        image = CTkImage(dark_image=image, light_image=image, size=(600, 500))
        CTkLabel(frame2, image=image, text="").pack()

        frame2.pack_propagate(False)
        frame2.pack(side="left")


class RegistrationPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        frame = CTkFrame(self, border_color="red", border_width=5, width=600, height=500)
        CTkLabel(frame, text='Register').pack(pady=10)
        CTkLabel(frame, text='Name').pack(pady=10)

        name = CTkEntry(frame)
        name.pack()

        CTkLabel(frame, text='Surname').pack(pady=10)

        surname = CTkEntry(frame)
        surname.pack()

        CTkLabel(frame, text='Email').pack(pady=10)

        email = CTkEntry(frame)
        email.pack()

        CTkLabel(frame, text='Password').pack(pady=10)

        password = CTkEntry(frame, show="*")
        password.pack(pady=10)

        button = CTkButton(frame, text='Register', hover_color="green")
        button.bind('<Button-1>', lambda event: self.controller.__handle_reg(
            {"name": name.get(), "surname": surname.get(), "email": email.get(), "password": password.get()}))
        button.pack(pady=10)

        back = CTkButton(frame, text='Back to login page', command=lambda: self.controller.show_frame(StartPage))
        back.pack(pady=10)
        frame.pack_propagate(False)
        frame.pack(side="right")


class Cabinet(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = CTkFrame(self, border_color="red", border_width=5)


        # CTkLabel(frame, text=f'Welcome {self.controller._user['name']}').pack()

        btn = CTkButton(frame, text='Log Out', command=lambda: controller.show_frame(StartPage))
        btn.bind('<Button-1>', lambda event: self.controller._user.clear())
        btn.pack()

        passwd = CTkButton(frame, text='Change My Password')
        passwd.bind('<Button-1>', lambda event: self.controller.__widget(textbox=True, cancel=True,
                                                                         function=self.controller.__cursor.change_password))
        passwd.pack()

        delete = CTkButton(frame, text='Delete My Account')
        delete.bind('<Button-1>', lambda event: self.controller.__widget(text="Are you sure?",
                                                                         function=lambda: self.controller.__cursor.delete_account(
                                                                             self.controller._user)))
        delete.pack()

        frame.pack(side="right")


