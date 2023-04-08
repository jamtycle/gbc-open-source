import datetime
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime as dt
from tkinter import messagebox

import db
from Views.AddExpense import AddExpenseFrame

MONTHS = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


def loadCombo(_combo: ttk.Combobox, _data):
    _combo["values"] = _data
    _combo.current(0)


class MainFrame:
    def __init__(self, master: tk.Tk, _user: list):
        master.wm_title("Main")
        self.user = _user
        self.result = None
        # build ui
        frame5 = ttk.Frame(master)
        frame5.configure(height=200, padding=20, width=300)
        label5 = ttk.Label(frame5)
        label5.configure(text=f"User: {self.user[1]}")
        label5.grid(column=0, row=0, rowspan=2, sticky="w")
        button9 = ttk.Button(frame5)
        button9.configure(text="Filter", command=lambda wid="btn_register": self.filterGrid())
        button9.grid(column=3, padx=10, row=0, rowspan=2)
        button10 = ttk.Button(frame5)
        button10.configure(text="Add Expense", command=lambda wid="btn_register": self.addNewExpense())
        button10.grid(column=0, row=3)
        self.btn_remove = ttk.Button(frame5)
        self.btn_remove.configure(text="Remove Expense", command=lambda wid="btn_register": self.removeExpense())
        self.btn_remove.grid(column=1, padx=8, row=3, sticky="w")
        button12 = ttk.Button(frame5)
        button12.configure(text="Log out", command=lambda wid="btn_register": self.logOut())
        button12.grid(column=6, row=3, sticky="e")
        self.cb_months = ttk.Combobox(frame5, state="readonly")
        self.cb_months.grid(column=2, padx=5, row=0, rowspan=2)
        self.cb_categories = ttk.Combobox(frame5, state="readonly")
        self.cb_categories.grid(column=1, padx=5, row=0, rowspan=2)
        self.data_type = tk.StringVar(value="raw")
        self.rb_weekly = ttk.Radiobutton(frame5)
        self.rb_weekly.configure(text="Weekly", value="weekly", variable=self.data_type, command=lambda: self.reportType())
        self.rb_weekly.grid(column=5, padx=10, row=0, sticky="w")
        self.rb_monthly = ttk.Radiobutton(frame5)
        self.rb_monthly.configure(text="Monthly", value="monthly", variable=self.data_type, command=lambda: self.reportType())
        self.rb_monthly.grid(column=5, padx=10, row=1, sticky="w")
        self.rb_details = ttk.Radiobutton(frame5)
        self.rb_details.configure(text="Details", value="raw", variable=self.data_type, command=lambda: self.reportType())
        self.rb_details.grid(column=4, row=0, rowspan=2)
        self.tv_data = ttk.Treeview(frame5, show="headings")
        self.tv_data.configure(selectmode="extended")
        self.tv_data.grid(columnspan=6, row=2, sticky="nsew", pady=10)
        frame5.pack(side="top")
        frame5.grid_anchor("center")
        frame5.rowconfigure(2, weight=5)

        # Main widget
        self.mainwindow = frame5
        loadCombo(self.cb_categories, tuple(db.getCategories()))
        loadCombo(self.cb_months, MONTHS)
        self.cb_months.current(dt.today().month)
        self.configGrid()
        self.loadGrid()

    def clearGrid(self):
        self.tv_data.delete(*self.tv_data.get_children())
        self.tv_data["displaycolumns"] = ()
        self.tv_data["columns"] = ()

    def configGrid(self):
        # self.tv_data.delete(self.tv_data.heading())
        # headers
        headers = db.getExpensesHeader(self.data_type.get())
        self.tv_data["columns"] = tuple(map(lambda x: x[0], headers))
        self.tv_data["displaycolumns"] = tuple(map(lambda x: x[0], filter(lambda x: x[2] > 0, headers)))
        # self.tv_data.column("#0", width=0)
        for i, h in enumerate(headers):
            self.tv_data.heading(i, text=h[1])
            self.tv_data.column(i, width=h[2])

    def loadGrid(self, _filter=None):
        # rows
        data = db.getExpenses(self.user[0], self.data_type.get())
        for i, row in enumerate(data):
            if _filter:
                if _filter(row):
                    self.tv_data.insert(parent="", index="end", text="1", values=row)
            else:
                self.tv_data.insert(parent="", index="end", text="1", values=row)

    def addNewExpense(self):
        window = tk.Tk()
        addframe = AddExpenseFrame(window)
        addframe.run()
        if not addframe.result:
            return

        if not db.addExpense(self.user[0], addframe.category_id, addframe.date, addframe.amount):
            messagebox.showerror("There was an error in the insertion process.")

        self.filterGrid()

    def removeExpense(self):
        sel = self.tv_data.selection()
        if not sel:
            return

        # print(self.tv_data.selection())
        row = self.tv_data.item(sel[0]).get("values")
        db.deleteExpense(row[0])
        self.filterGrid()

    def filterGrid(self):
        category_id = db.getCategoryID(self.cb_categories.get())
        month = MONTHS.index(self.cb_months.get())
        self.tv_data.delete(*self.tv_data.get_children())
        self.loadGrid(lambda row: self.filterLogic(row, category_id, month))

    def filterLogic(self, _row: list, _category_id: int, _month: int) -> bool:
        if self.data_type.get() == "raw":
            date = dt.strptime(_row[3], "%d-%m-%Y")
            if self.cb_categories.get().lower() == "all" and self.cb_months.get().lower() == "all":
                return True
            if self.cb_categories.get().lower() == "all":
                return date.month == _month
            if self.cb_months.get().lower() == "all":
                return _row[1] == _category_id

            return _row[1] == _category_id and date.month == _month
        elif self.data_type.get() == "monthly":
            # year = _row[2][0:_row[2].index("-")]
            month = int(_row[2][_row[2].index("-") + 1:len(_row[2])])
            if self.cb_categories.get().lower() == "all" and self.cb_months.get().lower() == "all":
                return True
            if self.cb_categories.get().lower() == "all":
                return month == _month
            if self.cb_months.get().lower() == "all":
                return _row[0] == _category_id

            return _row[0] == _category_id and month == _month
        elif self.data_type.get() == "weekly":
            year = int(_row[2][0:_row[2].index("-")])
            week = int(_row[2][_row[2].index("-") + 1:len(_row[2])])
            first_day = datetime.date(year, 1, 1)
            month = int((first_day + datetime.timedelta(weeks=week, days=-first_day.weekday())).strftime("%m"))

            if self.cb_categories.get().lower() == "all" and self.cb_months.get().lower() == "all":
                return True
            if self.cb_categories.get().lower() == "all":
                return month == _month
            if self.cb_months.get().lower() == "all":
                return _row[0] == _category_id

            return _row[0] == _category_id and month == _month

    def logOut(self):
        self.mainwindow.quit()
        self.mainwindow.destroy()
        self.result = "logout"

    def run(self):
        self.mainwindow.mainloop()

    def reportType(self):
        # print(self.data_type)
        self.clearGrid()
        self.configGrid()
        if self.data_type.get() != "raw":
            self.btn_remove["state"] = "disabled"
        else:
            self.btn_remove["state"] = "normal"
        self.filterGrid()


