import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import db

HEIGHT = 200
WIDTH = 300


class LoginFrame:
    def __init__(self, master: tk.Tk):
        master.wm_title("Login")
        self.loggedCallback = None
        # build ui
        frame1 = ttk.Frame(master)
        frame1.configure(height=HEIGHT, padding=20, width=WIDTH)
        label1 = ttk.Label(frame1)
        label1.configure(text="username")
        label1.grid(column=0, columnspan=2, row=0)
        entry1 = ttk.Entry(frame1)
        self.username = tk.StringVar()
        entry1.configure(textvariable=self.username)
        entry1.grid(column=0, columnspan=2, pady=0, row=1)
        label2 = ttk.Label(frame1)
        label2.configure(text="password")
        label2.grid(column=0, columnspan=2, row=2)
        entry2 = ttk.Entry(frame1)
        self.password = tk.StringVar()
        entry2.configure(show="•", textvariable=self.password)
        entry2.grid(column=0, columnspan=2, pady=0, row=3)
        self.btn_register = ttk.Button(frame1)
        self.btn_register.configure(text="Register")
        self.btn_register.grid(column=0, pady=10, padx=5, row=4)
        self.btn_register.configure(command=lambda wid="btn_register": self.registerAction())
        self.btn_login = ttk.Button(frame1)
        self.btn_login.configure(text="Log in")
        self.btn_login.grid(column=1, pady=10, padx=5, row=4)
        self.btn_login.configure(command=lambda wid="btn_login": self.loginAction())
        frame1.pack(side="top")

        # Main widget
        self.mainwindow = frame1

    def run(self):
        self.mainwindow.mainloop()

    def stop(self):
        self.mainwindow.quit()
        self.mainwindow.destroy()

    def validateInput(self) -> bool:
        if len(self.username.get()) == 0:
            messagebox.showwarning("Log in", "Username is empty.")
            return False
        if len(self.password.get()) == 0:
            messagebox.showwarning("Log in", "Password is empty.")
            return False
        return True

    def registerAction(self):
        if len(self.username.get()) == 0 and len(self.password.get()) == 0:
            messagebox.showinfo("Register", "Please provide a username and password in the fields above.")
            return

        if not self.validateInput():
            return

        if not messagebox.askyesno("Register", "Are you sure to create this user?"):
            return

        reg = db.userRegister(self.username.get(), self.password.get())
        if reg:
            messagebox.showerror("Register", reg)
        else:
            messagebox.showinfo("Register", f"User: '{self.username.get()} was created successfully")

    def loginAction(self):
        if not self.validateInput():
            return

        log = db.userLogin(self.username.get(), self.password.get())
        if not log:
            messagebox.showwarning("Log in", "Wrong username or password.")
            return

        self.stop()
        if self.loggedCallback:
            self.loggedCallback(log[0])
        # messagebox.showinfo("Log in", "Log in successfully.")
