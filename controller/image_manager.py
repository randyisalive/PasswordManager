from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename
import os
from services.image_manager import *
from services.misc import byteToMB

image_manager = Blueprint("image_manager", __name__)


TEMPLATE_ROUTE = "image-manager/"

route = "static/img/users/"


@image_manager.route("/image-manager<id>", methods=["POST", "GET"])
def index(id):
    id = session["id"]
    make_user_folder()  # make user folder to store image
    album = get_user_album(id)  # get user image image for displaying to web
    complete_route = route + session["username"]
    session.pop("image_id", None)  # remove image_id value in session
    return render_template(
        TEMPLATE_ROUTE + "index.html", album=album, complete_route=complete_route, id=id
    )


@image_manager.route("/image-manager/<album_id>", methods=["POST", "GET"])
def detail(album_id):
    user_id = session.get("id")
    images = get_user_image(user_id, album_id)
    return render_template(
        TEMPLATE_ROUTE + "detail.html", images=images, album_id=album_id
    )


@image_manager.route("/image-manager/select/<user_id><album_id>")
def select(user_id, album_id):
    user_id = session.get("id")
    images = get_user_image(user_id, album_id)
    if images == []:
        return redirect(url_for("image_manager.upload_image", album_id=album_id))
    return render_template(TEMPLATE_ROUTE + "select.html", images=images)


@image_manager.route("/image-manager/upload/<album_id>", methods=["POST", "GET"])
def upload_image(album_id):
    if request.method == "POST":
        file = request.files["image"]
        image_name = request.form["image_name"]
        filename = secure_filename(file.filename)  # get file name
        file_size = len(file.read())  # get file size
        id = session["id"]  # get id user from session
        folder_route = "static/img/users/" + session["username"]
        up_image(
            filename, id, image_name, album_id, file_size
        )  # upload image to server
        save_image_to_folder(
            filename, folder_route, file
        )  # copy and paste image to folder
        return redirect(url_for("image_manager.index", id=id))
    return render_template(TEMPLATE_ROUTE + "form.html")


@image_manager.route("/image-manager/delete")
def delete():
    folder_route = "static/img/users/" + session["username"]
    id = session["id"]
    image = get_user_image(id)  # get image id
    if image:
        if session.get("image_id"):
            id = session["image_id"]
            image_name = session["file_name"]
            delete_user_image(id)  # delete user image
            session.pop(
                "image_id", None
            )  # after delete, pop the image id so it is not in session
            os.remove(
                folder_route + "/" + image_name
            )  # remove image after being deleted by
            return redirect(url_for("image_manager.index"))
    else:
        error = "Image ID is None"
        return error
    error = "Image is None"
    return error


@image_manager.route("/album<id>", methods=["POST", "GET"])
def album(id):
    if not session:
        return redirect("auth.login")
    id = session.get("id")
    if request.method == "POST":
        title = request.form["title"]
        if title == "":
            error = "Insert title"
            return redirect(url_for("image_manager.album", id=id, error=error))
        add_album(title, id)
        return redirect(url_for("image_manager.index", id=id))

    return render_template(TEMPLATE_ROUTE + "album.html", id=id)
