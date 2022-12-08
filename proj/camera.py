from flask import Flask, render_template, Response, send_file

import atexit
import os
import numpy 

SHUTDOWN = "/shutdown"
app = Flask(__name__)


def gen_frames(): 
    #camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream') 
    while True:
            os.system('fswebcam -r "384x288" frame.jpeg')
            with open("frame.jpeg", "rb") as image:
                f = image.read()
                buffer = bytearray(f) 
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n')  # concat frame one by one and show result



@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    # os.system('fswebcam --jpeg 50 frame.jpeg') # uses Fswebcam to take picture pra definir compressao --jpeg 50 
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')




def OnExitApp():
    print('fechou')


if __name__ == '__main__':
    atexit.register(OnExitApp)
    os.system("camera_in") 
    #camera = cv2.VideoCapture(0) 
    app.run(host='0.0.0.0')

