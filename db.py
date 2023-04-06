import os
import sqlite3

DBNAME = "expenses.db"


def getExpenses(_con: sqlite3.Connection, _user_id: int):
    if not _con:
        return

    sql = "SELECT * FROM expenses WHERE _user_id = ?"
    return _con.cursor().execute(sql, [_user_id]).fetchall()


def userLogin(_con: sqlite3.Connection, _username: str, _password: str):
    if not _con:
        return

    sql = "SELECT * FROM users WHERE username = ? AND password = ?"
    res = _con.cursor().execute(sql, [_username, _password]).fetchall()
    return len(res) == 1


def userRegister(_con: sqlite3.Connection, _username: str, _password: str):
    if not _con:
        return

    sql = "INSERT INTO users VALUES (?, ?)"
    cur = _con.cursor().executemany(sql, [(_username, _password)])
    _con.commit()
    cur.close()
    return True





# add record to expenses table
def addRecord(_con: sqlite3.Connection, _user_id: int, _category_id: int, _date: str, _amount: float):
    if not _con:
        return

    sql = "INSERT INTO users expenses (_user_id, _category_id, _date, _amount ) VALUES (?,?,?,?)"
    cur = _con.cursor().execute(sql, (_user_id, _category_id, _date, _amount))
    _con.commit()
    cur.close()
    return True

# delete from expenses table
def deleteRecord(_con: sqlite3.Connection, _expense_id: int):
    if not _con:
        return

    sql = "DELETE FROM expenses WHERE id = ?"
    cur = _con.cursor().execute(sql, [_expense_id])
    _con.commit()
    cur.close()
    return True



def createDatabase(_con: sqlite3.Connection):
    if not _con:
        return

    sql = """
    CREATE TABLE users
    (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    );
    
    CREATE TABLE categories
    (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT
    );
        
    CREATE TABLE expenses
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_id INTEGER,
        date TEXT,
        amount REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    ); 
    
    INSERT INTO categories
    VALUES ('food'), 
           ('clothing'), 
           ('entertainment'), 
           ('rent'), 
           ('transportation'), 
           ('others'),
    """
    _con.cursor().execute(sql).close()
    print("Database tables created successfully.")


def getDBConnection():
    return sqlite3.connect(DBNAME)
