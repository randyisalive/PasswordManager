# Textbin controller
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from db import db_connection
from services.textbin import *


text = Blueprint("text", __name__)


@text.route("/<id>", methods=["GET"])
def index(id):
    S = ["Basic", "Code", "Important"]
    num = 0
    id = session.get("id")
    text = textbin(id)
    return render_template("textbin/index.html", text=text, id=id, S=S, num=num)


@text.route("/create", methods=["POST", "GET"])
def create():
    if not session:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        subject = request.form.get("subject")
        text = request.form.get("text")
        radio = request.form.get("filter")
        id = session.get("id")
        db = db_connection()
        cur = db.cursor()
        params = (text, id, subject, radio)
        cur.execute(
            "INSERT INTO textbin (text, user_id, subject, filter) VALUES (?,?,?,?)",
            params,
        )
        db.commit()
        cur.close()
        db.close()
        return redirect("text.index")

    return render_template("textbin/create.html")


# Textbin, function to see detail of the text content
@text.route("/<text>/<id>", methods=["POST", "GET"])
def detail(id, text):
    if not session:
        return redirect("auth.login")
    if request.method == "POST":
        db = db_connection()
        cur = db.cursor()
        content = request.form["content"]
        cur.execute("UPDATE textbin SET text = ? WHERE id = ?", (content, id))
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for("text.index", id=id))
    db = db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM textbin WHERE id =  ?", (id,))
    text_content = cur.fetchone()
    cur.close()
    db.close()

    return render_template("textbin/detail.html", text_content=text_content, id=id)


# To delete the selected text content
@text.route("/text-delete/<id>", methods=["POST", "GET"])
def delete(id):
    if not session:
        return redirect("auth.login")
    db = db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM textbin WHERE id = %s " % (id))
    cur.close()
    db.commit()
    return redirect(url_for("text.index", id=id))
