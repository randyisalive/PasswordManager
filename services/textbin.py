from db import db_connection


def textbin(id):
    db = db_connection()
    cur = db.cursor()
    cur.execute('SELECT * FROM textbin WHERE user_id = ?', (id, ))
    text = cur.fetchall()
    cur.close()
    db.close()
    return text
