from flask import Blueprint, render_template, redirect, request, session, url_for
from db import db_connection
from werkzeug.utils import secure_filename
from services.account_setting import (
    get_total_text_from_user,
    get_total_pass_from_user,
    get_total_image_from_user,
)
import os

account = Blueprint("account", __name__)

route = "/static\img"
templates_route = "account_details/"


@account.route("/account/<id>", methods=["POST", "GET"])
def index(id):
    username = str(session.get("username")).strip().capitalize()
    USER_DIRECTORY = (
        "/static/img/users/" + username + "/pp/" + str(session.get("profile_picture"))
    )

    PP_DIRECTORY = "static/img/users/" + username + "/pp"

    # Create profile_picture directory if not exist yet (for storing profile picture image)
    if os.path.exists(PP_DIRECTORY):
        pass
    else:
        os.mkdir(
            "static/img/users/"
            + str(session.get("username")).strip().capitalize()
            + "/pp/"
        )
    # Create profile_picture directory if not exist yet (for storing profile picture image)

    db = db_connection()
    cur = db.cursor()
    id = session.get("id")
    params = id
    sql = "SELECT * FROM users WHERE id = %s" % params
    cur.execute(sql)
    user = cur.fetchone()
    cur.close()
    total_text = get_total_text_from_user(id)
    total_images = get_total_image_from_user(24)
    total_pass = get_total_pass_from_user(id)
    filename = route + session["profile_picture"]
    db.close()
    return render_template(
        templates_route + "account_details.html",
        user=user,
        filename=filename,
        total_text=total_text,
        id=id,
        total_pass=total_pass,
        total_images=total_images,
        USER_DIRECTORY=USER_DIRECTORY,
    )


@account.route("/account/changepicture/<id>", methods=["POST", "GET"])
def changePP(id):
    username = str(session.get("username")).strip().capitalize()
    file_route = (
        "static/img/users/" + str(session["username"]).strip().capitalize() + "/pp/"
    )
    id = session.get("id")  # Get user ID
    if request.method == "POST":
        file = request.files["image"]
        filename = secure_filename(file.filename)
        db = db_connection()
        cur = db.cursor()
        params = (filename, id)
        sql = "UPDATE users SET profile_picture = '%s' WHERE id='%s'" % params
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
        if os.path.exists(file_route):
            file.save(os.path.join(file_route, filename))
            session.clear()
        else:
            os.mkdir(file_route)
            file.save(os.path.join(file_route, filename))
            session.clear()

        return redirect(url_for("auth.login"))
    return render_template(templates_route + "changePP.html", os=os)
