from flask import Flask, render_template, Response
#import atexit
import os 
import socket
host = "/tmp/9Lq7BNBnBycd6nxy.socket"
app = Flask(__name__)
global sock
global status
status = False
ultimo_bot = False
def controle():
    #print('tentando mudar')
    global status
    while True:
        #print('inicio do loop')
        if not status:
            #print('LIGAR')
            sock.sendall(bytes('L', "utf-8"))
            status = not status
            #print(status)
            yield ('', 204)
        else:
            #print('DESLIGAR')
            sock.sendall(bytes('D', "utf-8"))
            status = not status
            #print(status)
            yield ('', 204)


@app.route('/muda')
def muda():
    return next(controle())

@app.route("/status")
def botaoApertado():
    global status
    global ultimo_bot
    sock.sendall(bytes('O', "utf-8"))
    received = str(sock.recv(1024), "utf-8")
    if received== 'P':
        if not ultimo_bot:
            status = not status
            ultimo_bot=True
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if status:
        led = 'T'
    else:
        led = 'F'
    return {"botao": received, 'led': led}


@app.route('/')
def index():
    #(controle())
    return render_template('index.html')



def OnExitApp():
    print('@@@@@@@@@@@@@@@@@22')
    print('fechou')


if __name__ == '__main__':
    #atexit.register(OnExitApp)
    #os.system('./main')
    #print('2222222222222222')
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect((host))
    app.run(host='0.0.0.0')
