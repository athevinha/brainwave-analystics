
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from flask import render_template
# ========================================================
import random
import time
from cortex2 import EmotivCortex2Client
from paho.mqtt import client as mqtt_client
# ========================================================
url = "wss://localhost:6868"
emotive = None
profile_name = "FakeBCI"
CLIENT_ID = "bhOr0ZmsLWZVDeFl0QHE08e05lDI36blefUxfbLX"
CLIENT_SECRET = "BL3OlfhwzzPMXcxgFYT7uxaB6LSEAlwdLfqU4OG2oRJkRbQg63h4KMpvNp3144pOsybUpNLDrPQXuDXRC18oyIQUxh6Jum9ktR3nTNwChLW1ZdCcpzcuaavycLD000wK"
STREAM = "com"
# ==================================================================


def connect_cortexAPI():
    global emotive
    emotive = EmotivCortex2Client(url,
                                  client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  check_response=True,
                                  authenticate=True,
                                  debug=False)


def get_com_emotiv():
    global emotive
    emotive.request_access()
    emotive.authenticate()
    emotive.query_headsets()
    emotive.connect_headset(0)
    emotive.create_session(0)
    emotive.load_profile(profile_name)
    emotive.subscribe(streams=[STREAM])
    emotive.mental_command_action_sensitivity("get", profile_name)


# ========================================================
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('index.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('onconnect')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('onconnect', json, callback=messageReceived)
    return "hi"


@socketio.on('updatedata')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    while(True):
        upload_data()


def upload_data():
    global emotive
    if(emotive):
        emotive.mental_command_action_sensitivity("get", profile_name)
        data = emotive.receive_data()[STREAM]
        data_str = data[0]
        data_num = data[1]
        print(data)
        socketio.emit('updatedata', {'str': data_str,
                                     'num': data_num})
        socketio.sleep(0.125)


if __name__ == '__main__':
    connect_cortexAPI()
    get_com_emotiv()
    socketio.run(app, debug=False)
