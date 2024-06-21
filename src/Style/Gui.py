from customtkinter import *
from CTkMessagebox import CTkMessagebox
from src.dbo.actions import Actions
from src.Entities.User import User
from PIL import Image


class App(CTk):
    def __init__(self, grid="1000x500", **kwargs):
        super().__init__(**kwargs)
        self.resizable(False, False)
        self.geometry(grid)
        self.title("Db Manager")
        self.user = User()
        self.iconbitmap("Style/images/database.ico")
        self.cursor = Actions()
        self._set_appearance_mode("dark")
        self.container = CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.create_frame((StartPage, RegistrationPage, Cabinet))

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def create_frame(self, cont: tuple):
        for F in cont:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # TODO throws exception if executed and master window closes
    # def __widget(self, text: str = None, function: callable(object) = None):
    #     root = CTk()
    #     width = len(text) * 10
    #     height = width/1.5
    #     # root.attributes("-topmost", True)
    #     widget = CTkToplevel(root)
    #     widget.geometry(f"{width}x{height}")
    #     widget.title("Message")
    #     widget.resizable(False, False)
    #     CTkButton(widget, text="Cancel", command=widget.destroy).pack()
    #     if function is none:
    #         CTkButton(widget, text="Ok", command=widget.destroy).pack()
    #     button = CTkButton(widget, text="Ok", command=function())
    #     button.pack()

    # def __cls(self):
    #     for widget in self.winfo_children():
    #         widget.destroy()

    def handle_login(self, usr: User):
        try:
            self.user = self.cursor.login(usr)
            self.create_frame((Cabinet,))
            self.show_frame(Cabinet)

        except Exception as e:
            CTkMessagebox(message=str(e), title="Error", icon="cancel")

    def handle_reg(self, usr: User):
        try:
            self.cursor.register(usr)
            CTkMessagebox(message="User registered successfully", title="Success", icon="check")
        except Exception as e:
            CTkMessagebox(message=str(e), title="Error", icon="cancel")

    def handle_password_change(self, usr: User):
        try:
            dialog = CTkInputDialog(text="Type in a new password:", title="Test")

            passwd = dialog.get_input()
            if passwd is None:
                return
            self.cursor.change_password(usr, passwd)
            CTkMessagebox(message="Password changed!", title="Success", icon="check")
            self.create_frame((StartPage, RegistrationPage, Cabinet))
            self.show_frame(StartPage)
        except Exception as e:
            CTkMessagebox(message=str(e), title="Error", icon="cancel")

    def handle_delete_account(self, usr: User):
        resp = CTkMessagebox(message="Are you sure?", title="Delete account", icon="warning", option_1="ok",
                             option_2="cancel")
        if resp.get() == "ok":
            self.cursor.delete_account(usr)
            self.user.reset()
            # this is to make sure user is reset in every instance
            self.create_frame((StartPage, RegistrationPage, Cabinet))
            self.show_frame(StartPage)


class StartPage(CTkFrame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        frame = CTkFrame(self, width=400, height=500)
        CTkLabel(frame, text='Log In').pack(side="top", pady=50)
        CTkLabel(frame, text='Email').pack(side="top", pady=10)

        email = CTkEntry(frame, width=300)
        email.pack(side="top")

        CTkLabel(frame, text='Password').pack(side="top", pady=10)

        password = CTkEntry(frame, show="*", width=300)
        password.pack(side="top", pady=10)

        button = CTkButton(frame, text='Log In')
        button.bind('<Button-1>',
                    lambda event: controller.handle_login(User(email=email.get(), password=password.get())))
        button.pack(side="top", pady=20)

        CTkLabel(frame, text="Don't have an account?").pack(pady=2)

        reg = CTkButton(frame, text='Register', command=lambda: controller.show_frame(RegistrationPage))
        reg.pack()

        frame.pack_propagate(False)
        frame.pack(side="right")

        frame2 = CTkFrame(self, width=600, height=500, border_color="red", border_width=1)
        image = Image.open("Style/Images/textile.jpg")
        image = CTkImage(dark_image=image, light_image=image, size=(600, 500))
        CTkLabel(frame2, image=image, text="").pack()

        frame2.pack_propagate(False)
        frame2.pack(side="left")


class RegistrationPage(CTkFrame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        frame = CTkFrame(self, width=400, height=500)
        CTkLabel(frame, text='Register').pack(pady=10)
        CTkLabel(frame, text='Name').pack(pady=10)

        name = CTkEntry(frame, width=250)
        name.pack()

        CTkLabel(frame, text='Surname').pack(pady=10)

        surname = CTkEntry(frame, width=250)
        surname.pack()

        CTkLabel(frame, text='Email').pack(pady=10)

        email = CTkEntry(frame, width=250)
        email.pack()

        CTkLabel(frame, text='Password').pack(pady=5)

        password = CTkEntry(frame, show="*", width=250)
        password.pack(pady=10)

        button = CTkButton(frame, text='Register', hover_color="green")
        button.bind('<Button-1>', lambda event: controller.handle_reg(
            User(name=name.get(), surname=surname.get(), email=email.get(), password=password.get())))
        button.pack(pady=10)

        back = CTkButton(frame, text='Back to login page', command=lambda: controller.show_frame(StartPage))
        back.pack(pady=10)
        frame.pack_propagate(False)
        frame.pack(side="right")
        left_frame = CTkFrame(self, width=700, height=500)
        image = Image.open("Style/Images/a.jpg")
        image = CTkImage(dark_image=image, light_image=image, size=(700, 500))
        CTkLabel(left_frame, image=image, text="").pack()
        left_frame.pack_propagate(False)
        left_frame.pack(side="left")


class Cabinet(CTkFrame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)

        main_frame = CTkFrame(self, width=1000, height=500)
        main_frame.pack(fill="both", expand=True)

        user_frame = CTkFrame(main_frame, width=400, height=500)
        user_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        welcome_label = CTkLabel(user_frame, text=f'Welcome {controller.user.name}')
        welcome_label.pack(pady=10)

        logout_btn = CTkButton(user_frame, text='Log Out', command=lambda: controller.show_frame(StartPage))
        logout_btn.bind('<Button-1>', lambda event: controller.user.reset())
        logout_btn.pack(pady=15)

        change_password_btn = CTkButton(user_frame, text='Change My Password')
        change_password_btn.bind('<Button-1>', lambda event: controller.handle_password_change(controller.user))
        change_password_btn.pack(pady=15)

        delete_account_btn = CTkButton(user_frame, text='Delete My Account')
        delete_account_btn.bind('<Button-1>', lambda event: controller.handle_delete_account(controller.user))
        delete_account_btn.pack(pady=15)

        user_frame.pack_propagate(False)

        scrollable_frame = CTkScrollableFrame(main_frame, width=600, height=500)
        scrollable_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        products = controller.cursor.get_products()

        for i, product in enumerate(products):
            product_label = CTkLabel(scrollable_frame, text=f"{product[1]} - ${product[3]:.2f}")
            product_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        scrollable_frame.pack_propagate(False)
