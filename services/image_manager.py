import os
from db import db_connection
from flask import session


def make_user_folder():
    if not session.get("username"):
        return None
    route = "static/img/users/" + str(session["username"])
    if not os.path.exists(route):
        os.mkdir(route)
    else:
        pass


def change_image_name(title, image_id):
    db = db_connection()
    cur = db.cursor()
    params = (title, image_id)
    sql = "UPDATE images SET image_name = '%s' WHERE id = '%s'" % params
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()
        

def get_user_image(id):
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT file_name, image_name, id FROM images WHERE users_id = %s" % (
        session["id"]
    )
    cur.execute(sql)
    images = cur.fetchall()
    return images


def get_detail_image(image_id):
    db = db_connection()
    cur = db.cursor()
    params = image_id
    sql = "SELECT * FROM images WHERE id = %s" % params
    cur.execute(sql)
    image = cur.fetchone()
    return image


def delete_user_image(image_id):
    db = db_connection()
    cur = db.cursor()
    id = session["image_id"]
    cur.execute("DELETE FROM images WHERE id = %s" % (id))
    cur.close()
    db.commit()


def up_image(filename, id, image_name):
    db = db_connection()
    cur = db.cursor()
    params = (filename, id, image_name)
    sql = (
        "INSERT INTO images (file_name, users_id, image_name) VALUES ('\%s', '%s','%s') "
        % params
    )
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


def save_image_to_folder(filename, route, file):
    if os.path.exists(route):
        file.save(os.path.join(route, filename))
    else:
        os.mkdir(route)
        file.save(os.path.join(route, filename))
