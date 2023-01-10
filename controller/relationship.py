from flask import Blueprint, session, redirect, render_template, request, url_for
from db import db_connection


relationship = Blueprint('relationship', __name__)

TEMPLATE_ROUTE = 'relationship/'


@relationship.route('/', methods=['GET'])
def index():
    id = session['id']
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT * FROM user_relationship WHERE user_first_id = %s AND friends = 1" % (
        id)
    cur.execute(sql)
    context = cur.fetchall()
    if context:
        # DISPLAY FRIENDS
        sql_1 = "SELECT users.id, users.username, user_relationship.user_second_id FROM users INNER JOIN user_relationship ON users.id = user_relationship.user_second_id WHERE user_relationship.user_first_id = %s" % (
            id)
        cur.execute(sql_1)
        friends = cur.fetchall()
        cur.close()
        db.close()
    else:
        error = 'No Friends, sorry'
        return render_template(TEMPLATE_ROUTE + 'index.html', error=error)
    return render_template(TEMPLATE_ROUTE + 'index.html', context=context, friends=friends)


@relationship.route('/<username>')
def detail(username):
    if not session:
        return redirect(url_for('auth.login'))
    db = db_connection()
    cur = db.cursor()
    sql = "SELECT * FROM users WHERE username = '%s'" % (username)
    cur.execute(sql)
    user = cur.fetchone()
    user_id = user[0]
    cur.execute("SELECT id FROM images WHERE users_id = %s" % (user_id))
    images = cur.fetchall()
    total_images = len(images)
    cur.execute("SELECT id FROM content WHERE user_id = %s" % (user_id))
    content = cur.fetchall()
    total_content = len(content)
    cur.execute("SELECT id FROM textbin WHERE user_id = %s" % (user_id))
    text = cur.fetchall()
    total_text = len(text)
    if user is None:
        return redirect(url_for('home.index'))
    cur.close()
    db.close()
    return render_template(TEMPLATE_ROUTE + 'details.html', user=user, total_images=total_images, total_content=total_content, total_text=total_text)


@relationship.route('/search_user')
def search():
    if not session:
        return redirect(url_for('auth.login'))
    search = request.args.get('search')
    if request.method == 'GET':

        search = request.args.get('search')
        db = db_connection()
        cur = db.cursor()
        sql = "SELECT username, id, profile_picture FROM users WHERE username = '%s'" % (
            search)
        cur.execute(sql)
        user = cur.fetchall()
        cur.execute(
            "SELECT profile_picture FROM users WHERE username = '%s'" % (search))
        pp = cur.fetchone()
        pp_str = str(pp)
        pp_str = pp_str.replace('(', '').replace(
            ')', '').replace("'", "").replace('\\', "").replace(',', '')
        total_search = len(user)
        cur.close()
        db.close()
        return render_template(TEMPLATE_ROUTE + 'search.html', search=search, user=user, total_search=total_search, pp=pp, pp_str=pp_str)

    return render_template(TEMPLATE_ROUTE + 'search.html', search=search, user=user)


@relationship.route('/add')
def add():
    db = db_connection()
    cur = db.cursor()
    id = session['id']
    id_2 = request.args.get('id_2')
    params = (id, id_2)
    sql = "INSERT INTO user_relationship (user_first_id, user_second_id, friends) VALUES ('%s','%s',1)" % params
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('relationship.index'))


@relationship.route('/delete')
def unfollow():
    db = db_connection()
    cur = db.cursor()
    id = request.args.get('id')
    params = (id)
    sql = "DELETE FROM user_relationship WHERE user_second_id = '%s'" % params
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('relationship.index'))
