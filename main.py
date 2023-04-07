from tkinter import *
from tkinter import ttk
import db
from Views.LoginFrame import LoginFrame


def main():
    window = Tk()
    window.resizable(False, False)
    showLogin(window)
    # createGrid(window, db.getExpenses())
    window.mainloop()


def showLogin(_root: Tk):
    login = LoginFrame(_root)
    login.loggedCallback = lambda u: onLoginSuccess(u)
    login.run()


def onLoginSuccess(_user):
    print(_user)


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

