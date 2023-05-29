import os
from db import db_connection
from flask import session

def make_user_folder():
    if not session.get('username'):
        return None
    route = 'static/img/users/' + str(session['username'])
    if not os.path.exists(route):
        os.mkdir(route)
    else:
        pass
    

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
    cur.close()
    db.close()
    return image


def delete_user_image(image_id):
    db = db_connection()
    cur = db.cursor()
    id = session["image_id"]
    image_name = session["file_name"]
    cur.execute("DELETE FROM images WHERE id = %s" % (id))
    cur.close()
    db.commit()
     
    