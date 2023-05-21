import json
import sqlite3
from os import path

Path = path.dirname(path.abspath(__file__)) + path.sep
db = sqlite3.connect(Path+'bot.db')

sql = db.cursor()

def Get(table, key, _tupe=None):
    if table == "all":
        data = []

        sql.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = sql.fetchall()

        if tables:
            for x in tables:
                sql.execute(f"SELECT value FROM '{x[0]}' WHERE name='{key}'")
                s = sql.fetchone()[0]

                if s:
                    data.append(json.loads(s))
        return data
            


    sql.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")

    if sql.fetchone():
        sql.execute(f"SELECT value FROM '{table}' WHERE name='{key}'")
        data = sql.fetchone()[0]

        if data and _tupe == "json":
            data = json.loads(data)
    
    else:
        data = {}

    return data

def Set(table, key, data, _tupe=None):
    sql.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
    
    if sql.fetchone() is None:
        sql.execute(f"CREATE TABLE IF NOT EXISTS '{table}' (name, value)")

        for x in ('admins', 'admin_roles', 'status', 'rooms', 'warn', 'ban'):
            sql.execute(f"INSERT INTO '{table}' (name, value) VALUES ('{x}','')")
        db.commit()

    if _tupe == "json":
        data = json.dumps(data)

    sql.execute(f"UPDATE '{table}' SET value='{data}' WHERE name='{key}'")
    db.commit()


#Set("id65", "warn", {"GolOveShKa32": 1}, "json")
#print(Get("id65", "warn", "json"))
#print(Get("all", "warn", "json"))
