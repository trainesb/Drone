from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import video_stream, controller, pid
