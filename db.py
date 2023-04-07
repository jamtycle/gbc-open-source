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


def getExpenses(_user_id: int) -> list:
    _con = getDBConnection()
    if not _con:
        return []

    sql = "SELECT * FROM expenses WHERE _user_id = ?"
    return _con.cursor().execute(sql, [_user_id]).fetchall()


def getExpensesByCategory(_user_id: int, _category_id: int) -> list:
    _con = getDBConnection()
    if not _con:
        return []

    sql = "SELECT * FROM expenses WHERE _user_id = ?"
    return _con.cursor().execute(sql, [_user_id]).fetchall()


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
            VALUES ('food'), 
                   ('clothing'), 
                   ('entertainment'), 
                   ('rent'), 
                   ('transportation'), 
                   ('others')
            """
        _con.cursor().execute(sql).close()

    print("Database tables created successfully.")


def getDBConnection() -> sqlite3.Connection:
    return sqlite3.connect(DBNAME)
