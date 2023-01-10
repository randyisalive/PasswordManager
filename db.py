import sqlite3
from flask import g

DATABASE = 'database.db'


def db_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
