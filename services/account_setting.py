from db import db_connection


def get_total_text_from_user(user_id):
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT COUNT(text) FROM textbin WHERE user_id= %s" % (user_id)
    cur.execute(sql)
    total = cur.fetchone()
    return total


def update_account_setting(id, username, email):
    db = db_connection()
    cur = db.cursor()
    cur.execute(
        "UPDATE users SET username = ?, email = ? WHERE id = ?", (username, email, id)
    )
    db.commit()
    cur.close()
    db.close()


def get_total_image_from_user(user_id):
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT COUNT(id) FROM images WHERE users_id = %s" % (user_id)
    cur.execute(sql)
    total = cur.fetchone()
    return total


def get_total_pass_from_user(user_id):
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT COUNT(id) FROM content WHERE user_id = %s" % (user_id)
    cur.execute(sql)
    total = cur.fetchone()
    return total
