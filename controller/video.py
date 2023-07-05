# Handling video manager


# import
from flask import Blueprint, url_for, session, request, redirect, render_template, g
import os
from werkzeug.utils import secure_filename
from services.video import *

video = Blueprint("video", __name__)

TEMPLATE_ROUTE = "/VideoManager/"
VIDEO_FOLDER = "static/video/"


def byteToMB(byte):
    megabytes = byte / 1024 / 1024
    return megabytes


@video.route("/")
def index():
    folder_route = "static/video/" + session.get("username")
    id = session.get("id")  # get user id
    USER_FOLDER = VIDEO_FOLDER + str(session.get("username"))
    if not os.path.exists(USER_FOLDER):  # Check whether user video folder exist or not
        os.mkdir(USER_FOLDER)  # create the folder
    video = get_user_video(id)  # all user video
    return render_template(
        TEMPLATE_ROUTE + "index.html", video=video, folder_route=folder_route
    )


@video.route("/detail/<video_id>")
def detail(video_id):
    title = get_video_title(video_id)
    VIDEO_ROUTE = "/static/video/" + str(session.get("username")) + "/" + str(title[0])
    return render_template(TEMPLATE_ROUTE + "detail.html", VIDEO_ROUTE=VIDEO_ROUTE)


@video.route("/input", methods=["POST", "GET"])
def input():
    folder_route = "static/video/" + session.get("username")
    if request.method == "POST":
        file = request.files["video"]
        filename = secure_filename(file.filename)
        file_size = len(file.read())
        megabytes = byteToMB(file_size)  # convert byte to MB
        if megabytes > 150:  # limit file to only 150 MB
            return "File too big!!" + "File size: " + str(megabytes) + "MB"
        if filename == "":
            return redirect(url_for("video.input"))
        insert_video(session.get("id"), filename)
        save_video_to_folder(filename, folder_route, file)
        return redirect(url_for("video.index"))

    return render_template(TEMPLATE_ROUTE + "input.html")
