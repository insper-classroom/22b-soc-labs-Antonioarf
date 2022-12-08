from flask import Flask, render_template, Response
#import atexit
import os 

host = "/tmp/9Lq7BNBnBycd6nxy.socket"
app = Flask(__name__)



@app.route('/liga')
def liga():
    print('tentando ligar')
    os.system('./liga')
    return ('', 204)


@app.route('/desliga')
def desliga():
    print('tentando apagar')
    os.system('./desliga')
    return ('', 204)

@app.route('/')
def index():
    return render_template('index.html')



def OnExitApp():
    print('@@@@@@@@@@@@@@@@@22')
    print('fechou')


if __name__ == '__main__':
    #atexit.register(OnExitApp)
    app.run(host='0.0.0.0')
