from db import db_connection
from flask import request, redirect, render_template, session


def list_all_content(id):
    db = db_connection()
    cur = db.cursor()
    sql = 'SELECT * FROM content WHERE user_id = %s' % (id)
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    db.close()
    return content


def get_total_user_content(id):
    db = db_connection()
    cur = db.cursor()
    cur.execute('SELECT COUNT(id) FROM content WHERE user_id = ?', (id))
    total = cur.fetchone()
    cur.close()
    db.close()
    return total


def delete_password_by_id(id):
    db = db_connection()
    cur = db.cursor()
    cur.execute('DELETE FROM content WHERE id = ?', (id,))
    db.commit()
    cur.close()
    db.close()


def get_content_by_id(id):
    db = db_connection()
    cur = db.cursor()
    cur.execute('SELECT * FROM content WHERE id = ?', (id,))
    content = cur.fetchone()
    cur.close()
    db.close()
    return content
