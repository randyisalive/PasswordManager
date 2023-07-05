import os
from db import db_connection
from flask import session
from datetime import datetime

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
        

def get_user_image(user_id, album_id):
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT * FROM images WHERE album_id = ? AND users_id = ?"
    params = (album_id, user_id)
    cur.execute(sql, params)
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


def up_image(filename, id, image_name, album_id, file_size):
    db = db_connection()
    cur = db.cursor()
    date = datetime.now()
    params = (filename, id, image_name, date, album_id, file_size)
    sql = (
        "INSERT INTO images (file_name, users_id, image_name, posted_at, album_id, img_size) VALUES ('%s', '%s','%s', '%s', '%s', '%s') "
        % params
    )
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


def save_image_to_folder(filename, route, file):
    if os.path.exists(route):
        file.seek(0) # move the pointer to the start
        file.save(os.path.join(route, filename)) # save the file
    else:
        os.mkdir(route) # make folder
        file.seek(0) # move the pointer to the start
        file.save(os.path.join(route, filename)) # save the file


def add_album(title, id):
    db = db_connection()
    cur = db.cursor()
    params = (title, id)
    cur.execute('INSERT INTO album (title, user_id) VALUES (?,?)', params)
    db.commit()
    cur.close()
    
def get_user_album(user_id):
    db = db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM album WHERE user_id = ?", (user_id,))
    album = cur.fetchall()
    cur.close()
    db.close()
    return album
    