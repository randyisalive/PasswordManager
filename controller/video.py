# Handling video manager


# import
from flask import Blueprint, session, request, redirect, render_template
import os
from services.video import *

video = Blueprint('video', __name__)
TEMPLATE_ROUTE = '/VideoManager/'
VIDEO_FOLDER = 'static/video/'

@video.route('/')
def index():
    id = session.get('id')
    USER_FOLDER = VIDEO_FOLDER + str(session.get('username'))
    if not os.path.exists(USER_FOLDER): # Check whether user video folder exist or not
        os.mkdir(USER_FOLDER) 
    video = get_user_video(id)
    return render_template(TEMPLATE_ROUTE + 'index.html', video=video)



@video.route('/detail/<video_id>')
def detail(video_id):
    title = get_video_title(video_id)
    VIDEO_ROUTE = '/static/video/' + str(session.get('username')) + "/" + str(title[0])    
    return render_template(TEMPLATE_ROUTE + 'detail.html', VIDEO_ROUTE=VIDEO_ROUTE)
