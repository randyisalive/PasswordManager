import math
from flask import (
    Blueprint, flash, render_template, request, session, url_for, redirect, g
)
from db import db_connection
from services.home import *
from controller.auth import *


home = Blueprint('home', __name__)


@home.route('/', methods=['POST', 'GET'])
def index():
    id = session.get('id')
    if id is None:
        return redirect(url_for('auth.login'))
    db = db_connection()
    cur = db.cursor()

    # pagination
    page = request.args.get('page', type=int, default=1)
    limit = 10
    if page > 1:
        first_page = (page * limit) - limit
        num = first_page + 1
        num_list = [num]
    else:
        first_page = 0
        num = first_page + 1
        num_list = [num]
    cur.execute("SELECT * FROM content WHERE user_id = %s" % (id))
    all_content = cur.fetchall()
    # Loop throug pagination
    total_pages = (int(len(all_content)) / limit) + 1
    total_pages = math.ceil(total_pages)
    params = (id, first_page, limit)
    sql = 'SELECT * FROM content WHERE user_id = %s LIMIT %s, %s' % params
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    db.close()
    return render_template('index.html', content=content, id=id, total_pages=total_pages, num_list=num_list)


@home.route('/delete/<id>', methods=['GET'])
def delete(id):
    db = db_connection()
    cur = db.cursor()
    cur.execute('DELETE FROM content WHERE id = ?', (id,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('home.index'))


@home.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@home.route('/add-pass', methods=['POST', 'GET'])
def add_pass():
    id = session.get('id')
    password_add = request.args.get('user_password')
    if request.method == 'POST':
        description = request.form['description']
        username = request.form['username']
        password = request.form['password']
        db = db_connection()
        cur = db.cursor()
        params = (password, description, username, id)
        cur.execute(
            'INSERT INTO content (password_site, site, username_site, user_id) VALUES (?,?,?,?)', params)
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for('home.index', id=id))
    return render_template('form.html', id=id, password_add=password_add)


@home.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    if not session:
        return redirect(url_for('auth.login'))
    error = ''
    if request.method == 'POST':
        site = request.form['site']
        email = request.form['email']
        password = request.form['password']
        db = db_connection()
        cursor = db.cursor()
        params = (password,  site, email, id)
        cursor.execute(
            "UPDATE content SET password_site = ?, site= ?, username_site= ? WHERE id= ? ", params)
        cursor.close()
        db.commit()
        db.close()
        return redirect(url_for('home.index', id=id))
    content = get_content_by_id(id)

    return render_template('edit.html', id=id, content=content)
