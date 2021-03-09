from flask import Flask
from flask import request
from flask import render_template
import random
import time
from cortex2 import EmotivCortex2Client
from paho.mqtt import client as mqtt_client
url = "wss://localhost:6868"
emotive = None
profile_name = "FakeBCI"
CLIENT_ID = "bhOr0ZmsLWZVDeFl0QHE08e05lDI36blefUxfbLX"
CLIENT_SECRET = "BL3OlfhwzzPMXcxgFYT7uxaB6LSEAlwdLfqU4OG2oRJkRbQg63h4KMpvNp3144pOsybUpNLDrPQXuDXRC18oyIQUxh6Jum9ktR3nTNwChLW1ZdCcpzcuaavycLD000wK"
STREAM = "com"


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


app = Flask(__name__)


@app.callback(
    Output('left'),
)
@app.route('/')
def left():
    data = "qweg"
    return render_template("index.html", data=data)


if __name__ == '__main__':
    connect_cortexAPI()
    get_com_emotiv()
    app.run()
