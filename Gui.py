import tkinter
from tkinter import ttk


class App(tkinter.Tk):
    def __init__(self, size: str = '1000x1000', title: str = 'Db Manager'):
        super().__init__()
        self.geometry(size)
        self.resizable(False, False)
        self.title(title)


    def loginpage(self, command: callable):
        label = ttk.Label(self, text='Log In')
        label.pack()
        entry = ttk.Entry(self)
        entry.pack()
        button = ttk.Button(self, text='Log In', command=command)
        button.pack()

        self.mainloop()
