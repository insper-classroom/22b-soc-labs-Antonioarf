from flask import Flask, render_template, Response
import cv2
import atexit

SHUTDOWN = "/shutdown"
app = Flask(__name__)





def gen_frames(): 
    #camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream') 
    while True:
        assert camera.isOpened()
        success, frame = camera.read()  # read the camera frame
        #frame = cv2.imread('frame.jpeg', 0) 
        #success = True
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')




def OnExitApp():
    #print('@@@@@@@@@@@@@@@@@22')
    camera.release()
    #cv2.destroyAllWindows()
    #print('fechou')


if __name__ == '__main__':
    atexit.register(OnExitApp)
    camera = cv2.VideoCapture(0) 
    app.run(host='0.0.0.0')
