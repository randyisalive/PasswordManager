from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

# Import controller module
from controller.home import *
from controller.auth import *
from controller.account import *
from controller.generator import *
from controller.image_manager import *
from controller.text import *
from controller.video import video

# Import controller module

# App config

app = Flask(__name__)


app.secret_key = "1"
app.debug = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


# App config

toolbar = DebugToolbarExtension(app)


app.register_blueprint(home, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(account, url_prefix="/")
app.register_blueprint(generator, url_prefix="/")
app.register_blueprint(image_manager, url_prefix="/")
app.register_blueprint(text, url_prefix="/textbin")
app.register_blueprint(video, url_prefix="/video")


if __name__ == "__main__":
    app.run()
