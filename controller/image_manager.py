from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    flash,
    send_from_directory,
    session,
    url_for,
)
from route import APP_ROOT
from db import db_connection
from werkzeug.utils import secure_filename
import os
from services.image_manager import *

image_manager = Blueprint("image_manager", __name__)


TEMPLATE_ROUTE = "image-manager/"

route = "static/img/users/"


@image_manager.route("/image-manager", methods=["POST", "GET"])
def index():
    make_user_folder() # make user folder to store image
    images = get_user_image(session['id']) # get user image image for displaying to web 
    complete_route = route + session["username"]
    session.pop("image_id", None) # remove image_id value in session
    return render_template(
        TEMPLATE_ROUTE + "index.html",
        image=images,
        complete_route=complete_route,
    )


@image_manager.route("/image-manager/detail/<image_id>")
def detail(image_id):
    image = get_detail_image(image_id)
    file_name = image[1]
    session["image_id"] = image_id
    file_name = str(file_name)
    strFileName = file_name.replace("\\", "")
    session["file_name"] = strFileName
    username = str(session["username"])
    string_username = username.strip().capitalize()
    file_route = "static/img/users/" + string_username
    return render_template(
        TEMPLATE_ROUTE + "detail.html",
        image=image,
        file_route=file_route,
        strFileName=strFileName,
    )


@image_manager.route("/image-manager/upload", methods=["POST", "GET"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]
        image_name = request.form["image_name"]
        filename = secure_filename(file.filename)
        id = session["id"]
        db = db_connection()
        cur = db.cursor()
        file_route = "static/img/users/" + session["username"]
        params = (filename, id, image_name)
        sql = (
            "INSERT INTO images (file_name, users_id, image_name) VALUES ('\%s', '%s','%s') "
            % params
        )
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
        if os.path.exists(file_route):
            file.save(os.path.join(file_route, filename))
        else:
            os.mkdir(file_route)
            file.save(os.path.join(file_route, filename))
        return redirect(url_for("image_manager.index"))
    return render_template(TEMPLATE_ROUTE + "form.html")


@image_manager.route("/image-manager/delete")
def delete():
    file_route = "static/img/users/" + session["username"]
    id = session["id"]
    image = get_user_image(id)
    if image:
        if session.get("image_id"):
            id = session["image_id"]
            image_name = session["file_name"]
            delete_user_image(id) # delete user image
            session.pop("image_id", None) # after delete, pop the image id so it is not in session
            os.remove(file_route + "/" + image_name) # remove image after being deleted by 
            return redirect(url_for("image_manager.index"))
    else:
        error = "Image ID is None"
        return error
    error = "Image is None"
    return error
