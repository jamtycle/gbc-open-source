import datetime
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from tkcalendar import DateEntry

import db
import input_validation


class AddExpenseFrame:
    def __init__(self, master: tkinter.Tk):
        master.resizable(False, False)
        master.wm_title("Add Expense")
        self.result = None
        self.category_id = None
        self.date = None
        self.amount = None
        # build ui
        main = ttk.Frame(master)
        main.configure(height=200, padding=10, width=300)
        label15 = ttk.Label(main)
        label15.configure(
            anchor="center", justify="center", takefocus=False, text="Add Expense"
        )
        label15.pack(fill="x", side="top")
        separator6 = ttk.Separator(main)
        separator6.configure(orient="horizontal", takefocus=False)
        separator6.pack(fill="x", pady=10, side="top")
        label16 = ttk.Label(main)
        label16.configure(takefocus=False, text="Category")
        label16.pack(side="top")
        self.cb_category = ttk.Combobox(main)
        self.cb_category.configure(state="readonly")
        self.cb_category.pack(fill="x", side="top")
        label17 = ttk.Label(main)
        label17.configure(takefocus=False, text="Date")
        label17.pack(side="top")
        self.de_date = DateEntry(main, date_pattern="dd-mm-YYYY")
        self.de_date.configure(justify="left", state="readonly")
        self.de_date.pack(fill="x", side="top")
        label18 = ttk.Label(main)
        label18.configure(takefocus=False, text="Amount")
        label18.pack(side="top")
        self.tx_amount = ttk.Entry(main)
        self.tx_amount.configure()
        self.tx_amount.pack(fill="x", side="top")
        separator7 = ttk.Separator(main)
        separator7.configure(orient="horizontal")
        separator7.pack(fill="x", pady=10, side="top")
        frame12 = ttk.Frame(main)
        frame12.configure(height=200, width=200)
        button23 = ttk.Button(frame12)
        button23.configure(text="Cancel", command=lambda: self.cancelAction())
        button23.grid(column=1, padx=5, row=0)
        button24 = ttk.Button(frame12)
        button24.configure(text="Accept", command=lambda: self.acceptAction())
        button24.grid(column=0, padx=5, row=0)
        frame12.pack(side="top")
        main.pack(side="top")

        # Main widget
        self.mainwindow = main
        self.loadCategories()
        self.de_date.set_date(date=datetime.date.today())

    def run(self):
        self.mainwindow.mainloop()

    def loadCategories(self):
        categories = db.getCategories()
        categories.remove(('All',))
        self.cb_category["values"] = tuple(categories)
        self.cb_category.current(0)

    def cancelAction(self):
        self.mainwindow.master.quit()
        self.mainwindow.master.destroy()
        self.result = False

    def acceptAction(self):
        if not input_validation.validate_amount(self.tx_amount.get()):
            messagebox.showinfo("Add Expenses", "Amount was not in the correct format.")
            return

        self.category_id = db.getCategoryID(self.cb_category.get())
        self.date = self.de_date.get_date().strftime("%d-%m-%Y")
        self.amount = self.tx_amount.get()

        self.mainwindow.master.quit()
        self.mainwindow.master.destroy()
        self.result = True
