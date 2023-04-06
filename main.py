from tkinter import *
from tkinter import ttk


def main():
    window = Tk()
    for x in range(5):
        for y in range(4):
            frameGrid = Frame(master=window, relief=RAISED, borderwidth=2)
            frameGrid.grid(row=x, column=y)
            labelGrid = Label(master=frameGrid, text=f"Row No. {x}\nColumn No. {y}")
            labelGrid.pack()
    window.mainloop()


if __name__ == "__main__":
    main()

