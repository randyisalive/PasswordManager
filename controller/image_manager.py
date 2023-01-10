from flask import Blueprint, redirect, render_template, request, flash, send_from_directory, session, url_for
from route import APP_ROOT
from db import db_connection
from werkzeug.utils import secure_filename
from PIL import Image
import os

image_manager = Blueprint('image_manager', __name__)


TEMPLATE_ROUTE = 'image-manager/'

route = 'static\img\img_manager'


@image_manager.route('/image-manager', methods=['POST', 'GET'])
def index():
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT file_name, image_name, id FROM images WHERE users_id = %s" % (
        session['id'])
    cur.execute(sql)
    images = cur.fetchall()
    session.pop('image_id', None)
    return render_template(TEMPLATE_ROUTE + 'index.html', image=images, route=route)


@image_manager.route('/image-manager/detail/<image_id>')
def detail(image_id):
    db = db_connection()
    cur = db.cursor()
    params = (image_id)

    sql = 'SELECT * FROM images WHERE id = %s' % params
    cur.execute(sql)
    image = cur.fetchone()
    file_name = image[1]
    session['image_id'] = image_id
    file_name = str(file_name)
    strFileName = file_name.replace('\\', '')
    session['file_name'] = strFileName
    username = str(session['username'])
    string_username = username.strip().capitalize()
    file_route = "static/img/users/" + string_username
    cur.close()
    db.close()
    return render_template(TEMPLATE_ROUTE + 'detail.html', image=image, file_route=file_route, strFileName=strFileName)


@image_manager.route('/image-manager/upload', methods=['POST', 'GET'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        image_name = request.form['image_name']
        filename = secure_filename(file.filename)
        id = session['id']
        db = db_connection()
        cur = db.cursor()
        file_route = "static/img/users/" + session['username']
        params = (filename, id, image_name)
        sql = "INSERT INTO images (file_name, users_id, image_name) VALUES ('\%s', '%s','%s') " % params
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
        if os.path.exists(file_route):
            file.save(os.path.join(file_route, filename))
        else:
            os.mkdir(file_route)
            file.save(os.path.join(file_route, filename))
        return redirect(url_for('image_manager.index'))
    return render_template(TEMPLATE_ROUTE + 'form.html')


@image_manager.route('/image-manager/delete')
def delete():
    file_route = "static/img/users/" + session['username']
    id = session['id']
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT * FROM images WHERE users_id = %s " % (id)
    cur.execute(sql)
    image = cur.fetchall()
    if image:
        if session.get('image_id'):
            id = session['image_id']
            image_name = session['file_name']
            cur.execute("DELETE FROM images WHERE id = %s" % (id))
            cur.close()
            db.commit()
            session.pop('image_id', None)
            os.remove(file_route + '/' + image_name)
            return redirect(url_for('image_manager.index'))
    else:
        error = "Image ID is None"
        return render_template('404.html', error=error)
    error = "Image is None"
    return render_template('404.html', error=error)
