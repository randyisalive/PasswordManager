from db import db_connection
import os


def get_user_video(id):
    db = db_connection()
    cur = db.cursor()
    params = id
    sql = "SELECT * FROM video WHERE user_id = %s" % params
    cur.execute(sql)
    video = cur.fetchall()
    cur.close()
    db.close()
    return video


def get_video_title(video_id):
    db = db_connection()
    cur = db.cursor()
    params = video_id
    sql = "SELECT video_title FROM video WHERE id = %s" % params
    cur.execute(sql)
    video_title = cur.fetchone()
    cur.close()
    db.close()
    return video_title


def insert_video(user_id, video_title):
    db = db_connection()
    cur = db.cursor()
    params = (video_title, user_id)
    sql = "INSERT INTO video (video_title, user_id) VALUES (?,?)"
    cur.execute(sql, params)
    db.commit()
    cur.close()
    db.close()


def save_video_to_folder(filename, route, file):
    if os.path.exists(route):
        file.seek(0)  # move the pointer to the start
        file.save(os.path.join(route, filename))  # save the file
    else:
        os.mkdir(route)  # make folder
        file.seek(0)  # move the pointer to the start
        file.save(os.path.join(route, filename))  # save the file
