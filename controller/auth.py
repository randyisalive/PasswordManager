from flask import Blueprint, session, redirect, render_template, flash, url_for, request
from db import db_connection
import os

auth = Blueprint("auth", __name__)
folder_route = "static/img/users/"


@auth.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember = request.form["remember"]
        conn = db_connection()
        cur = conn.cursor()
        params = (username, password)
        sql = (
            "SELECT id, email, username, password, profile_picture FROM users WHERE username = '%s' AND password = '%s'"
            % params
        )
        cur.execute(sql)
        user = cur.fetchone()
        if user is None:
            error = "Wrong username or password"
        else:
            session.clear()
            session["id"] = user[0]
            session["username"] = user[2]
            session["email"] = user[1]
            session["profile_picture"] = user[4]
            return redirect(url_for("home.index"))
        flash(error)
        cur.close()
        conn.close()
    return render_template("login.html", error=error)


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        db = db_connection()
        cur = db.cursor()
        params = (email, username, password)
        cur.execute(
            "SELECT * FROM users WHERE username = ? AND email = ?", (username, email)
        )
        user = cur.fetchone()
        if user is None:
            username = username.strip().capitalize()
            user_folder = os.path.join(folder_route, username)
            path_user = folder_route + username  # static/img/users/USERNAME
            if os.path.exists(path_user):
                os.rmdir(path_user)
                os.mkdir(user_folder)
            else:
                os.mkdir(user_folder)
            cur.execute(
                "INSERT INTO users (email,username, password) VALUES (?,?,?)", params
            )
            db.commit()

            cur.close()
            db.close()

            return redirect(url_for("auth.login"))
        else:
            error = "User already exist!!!"
            return redirect(url_for("auth.signup", error=error))
    return render_template("signup.html")
