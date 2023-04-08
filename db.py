import sqlite3

DBNAME = "expenses.db"


def userLogin(_username: str, _password: str) -> list | None:
    _con = getDBConnection()
    if not _con:
        return None

    sql = "SELECT user_id, username FROM users WHERE username = ? AND password = ?"
    res = _con.cursor().execute(sql, [_username, _password]).fetchall()
    return res


def userRegister(_username: str, _password: str) -> str | None:
    _con = getDBConnection()
    if not _con:
        return "There was a problem with the database."

    if len(_con.cursor().execute("SELECT * FROM users WHERE username = ?", [_username]).fetchall()) != 0:
        return "The user already exist"

    sql = "INSERT INTO users(username, password) VALUES (?, ?)"
    cur = _con.cursor().executemany(sql, [(_username, _password)])
    _con.commit()
    cur.close()
    return None


def getExpensesHeader(_type: str) -> list:
    if not _type:
        return [
            ('id', "ID", 30),
            ('category_id', "CategoryID", 0),
            ('date', "Date", 150),
            ('amount', "Amount", 150),
        ]
    if _type == "weekly":
        return [
            ('category_id', "CategoryID", 0),
            ('category_name', "Category", 150),
            ('week', "Week", 150),
            ('amount', "Amount", 150),
        ]
    elif _type == "monthly":
        return [
            ('category_id', "CategoryID", 0),
            ('category_name', "Category", 150),
            ('month', "Month", 150),
            ('amount', "Amount", 150),
        ]
    elif _type == "raw":
        return [
            ('id', "ID", 30),
            ('category_id', "CategoryID", 0),
            ('category_name', "Category", 150),
            ('date', "Date", 150),
            ('amount', "Amount", 150),
        ]
    else:
        return [
            ('id', "ID", 30),
            ('category_id', "CategoryID", 0),
            ('date', "Date", 150),
            ('amount', "Amount", 150),
        ]


def getExpenses(_user_id: int, _type: str) -> list:
    _con = getDBConnection()
    if not _con:
        return []

    if not _type:
        sql = "SELECT * FROM expenses WHERE user_id = ? LIMIT 0"
    if _type == "weekly":
        sql = """
        SELECT   categories.category_id, categories.category_name, 
                 strftime("%Y-%W", date(datetime(substr(expenses.date, 7) || '-' || substr(expenses.date, 4, 2) || '-' || substr(expenses.date, 1, 2)))) AS week,
                 SUM(expenses.amount) AS amount
        FROM 	 expenses INNER JOIN categories ON expenses.category_id = categories.category_id
        WHERE    user_id = ?
        GROUP BY categories.category_id, categories.category_name, week
        """
    elif _type == "monthly":
        sql = """
        SELECT   categories.category_id, categories.category_name, 
                 strftime("%Y-%m", date(datetime(substr(expenses.date, 7) || '-' || substr(expenses.date, 4, 2) || '-' || substr(expenses.date, 1, 2)))) AS month,
                 SUM(expenses.amount) AS amount
        FROM 	 expenses INNER JOIN categories ON expenses.category_id = categories.category_id
        WHERE    user_id = ?
        GROUP BY categories.category_id, categories.category_name, month
        """
    elif _type == "raw":
        sql = """
                SELECT   expenses.id, categories.category_id, categories.category_name, expenses.date, expenses.amount
                FROM     expenses INNER JOIN categories ON expenses.category_id = categories.category_id
                WHERE    user_id = ?
                """
    else:
        sql = "SELECT * FROM expenses WHERE user_id = ? LIMIT 0"

    return _con.cursor().execute(sql, [_user_id]).fetchall()


def getExpensesByYear(_user_id: int, _year: int) -> list:
    _con = getDBConnection()
    if not _con:
        return []

    sql = """
        SELECT   -1, "Average" AS category_name,
                 strftime("%Y", date(datetime(substr(expenses.date, 7) || '-' || substr(expenses.date, 4, 2) || '-' || substr(expenses.date, 1, 2)))) AS year,
                 AVG(expenses.amount) AS amount
        FROM     expenses
        WHERE 	 user_id = ?
                 AND CAST(strftime("%Y", date(datetime(substr(expenses.date, 7) || '-' || substr(expenses.date, 4, 2) || '-' || substr(expenses.date, 1, 2)))) AS INTEGER) = ?
        GROUP BY 1, 2, 3
    """
    return _con.cursor().execute(sql, [_user_id, _year]).fetchall()[0]


def getExpensesByCategory(_user_id: int, _category_id: int) -> list:
    _con = getDBConnection()
    if not _con:
        return []

    sql = """
      SELECT   expenses.id, categories.category_id, categories.category_name, expenses.date, expenses.amount
      FROM     expenses INNER JOIN categories ON expenses.category_id = categories.category_id
      WHERE    user_id = ? AND
               category_id = ?
    """
    return _con.cursor().execute(sql, [_user_id, _category_id]).fetchall()


def addExpense(_user_id: int, _category_id: int, _date: str, _amount: float) -> bool:
    _con = getDBConnection()
    if not _con:
        return False

    sql = "INSERT INTO expenses(user_id, category_id, date, amount) VALUES (?, ?, ?, ?)"
    cur = _con.cursor().execute(sql, (_user_id, _category_id, _date, _amount))
    _con.commit()
    cur.close()
    return True


def deleteExpense(_expense_id: int) -> bool:
    _con = getDBConnection()
    if not _con:
        return False

    sql = "DELETE FROM expenses WHERE id = ?"
    cur = _con.cursor().execute(sql, [_expense_id])
    _con.commit()
    cur.close()
    return True


def getCategories() -> list:
    _con = getDBConnection()
    if not _con:
        return []

    sql = "SELECT category_name FROM categories"
    rows = _con.cursor().execute(sql).fetchall()
    return rows


def getCategoryID(_category_name: str) -> int | bool:
    _con = getDBConnection()
    if not _con:
        return False

    sql = "SELECT category_id FROM categories WHERE category_name = ?"
    data = _con.cursor().execute(sql, [_category_name]).fetchall()
    if len(data) == 0:
        return False
    return data[0][0]


def createDatabase():
    _con = getDBConnection()
    if not _con:
        return

    sql = """
    CREATE TABLE IF NOT EXISTS users 
    (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    );
    
    CREATE TABLE IF NOT EXISTS categories
    (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS expenses
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_id INTEGER,
        date TEXT,
        amount REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """
    _con.cursor().executescript(sql).close()

    if len(_con.cursor().execute("SELECT * FROM categories").fetchall()) == 0:
        sql = """
            INSERT INTO categories(category_name)
            VALUES ('All'),
                   ('Food'), 
                   ('Clothing'), 
                   ('Entertainment'), 
                   ('Rent'), 
                   ('Transportation'), 
                   ('Others')
            """
        cur = _con.cursor().execute(sql)
        _con.commit()
        cur.close()

    print("Database tables created successfully.")


def getDBConnection() -> sqlite3.Connection:
    return sqlite3.connect(DBNAME)
