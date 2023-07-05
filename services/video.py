from db import db_connection



def get_user_video(id):
    db = db_connection()
    cur = db.cursor()
    params = (id)
    sql = "SELECT * FROM video WHERE user_id = %s" % params
    cur.execute(sql)
    video = cur.fetchall()
    cur.close()
    db.close()
    return video


def get_video_title(video_id):
    db = db_connection()
    cur = db.cursor()
    params = (video_id)
    sql = "SELECT video_title FROM video WHERE id = %s" % params
    cur.execute(sql)
    video_title = cur.fetchone()
    cur.close()
    db.close()
    return video_title


