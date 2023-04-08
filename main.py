from tkinter import *
from tkinter import ttk

import screeninfo
from screeninfo import get_monitors

import Views.LoginFrame
import db
from Views.LoginFrame import LoginFrame
from Views.MainFrame import MainFrame


USER = []
WINDOW = Tk()


def main():
    WINDOW.resizable(False, False)
    showLogin(WINDOW)
    WINDOW.mainloop()


def onLoginSuccess(_user: tuple):
    global USER, WINDOW
    USER = _user
    showMain(WINDOW)


def showLogin(_root: Tk):
    login = LoginFrame(_root)
    login.loggedCallback = lambda u: onLoginSuccess(u)
    login.run()

    # print(getPrimaryScreen())
    # x_pos = (getPrimaryScreen().width // 2) - (Views.LoginFrame.WIDTH // 2)
    # y_pos = (getPrimaryScreen().height // 2) - (Views.LoginFrame.HEIGHT // 2)
    # print(x_pos)
    # print(y_pos)
    # # print(WINDOW.winfo_width())
    # # print(WINDOW.winfo_height())
    # print(Views.LoginFrame.WIDTH)
    # print(Views.LoginFrame.HEIGHT)
    # # WINDOW.positionfrom()
    # WINDOW.geometry('{}x{}+{}+{}'.format(Views.LoginFrame.WIDTH, Views.LoginFrame.HEIGHT, x_pos, y_pos))


def showMain(_root: Tk):
    main = MainFrame(_root, USER)
    main.run()
    if not main.result:
        return
    if main.result == "logout":
        showLogin(_root)


def getPrimaryScreen() -> screeninfo.Monitor:
    for m in get_monitors():
        if m.is_primary:
            return m


def createGrid(_root: Tk, _data: list):
    for x, row in enumerate(_data):
        for y, val in enumerate(row):
            frameGrid = Frame(master=_root, relief=RAISED, borderwidth=2)
            frameGrid.grid(row=x, column=y)
            labelGrid = Label(master=frameGrid, text=f"{val}")
            labelGrid.pack()


if __name__ == "__main__":
    db.createDatabase()
    main()

