from flask import Blueprint, render_template, redirect, request, session
from route import APP_ROOT
from db import db_connection

account = Blueprint('account', __name__)

route = "/static\img"


@account.route('/account')
def index():
    db = db_connection()
    cur = db.cursor()
    id = session.get('id')
    params = (id)
    sql = "SELECT * FROM users WHERE id = %s" % params
    cur.execute(sql)
    user = cur.fetchall()
    cur.close()
    db.close()
    filename = route + session['profile_picture']
    return render_template('account_details.html', user=user, filename=filename)
