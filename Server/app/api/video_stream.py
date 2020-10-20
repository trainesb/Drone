from app.api import bp
from flask import Response
from app.utils.camera_pi import Camera

@bp.route('/api/video_stream', methods=['GET'])
def video_stream():
    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
