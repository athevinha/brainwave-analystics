
import random
import time
from cortex2 import EmotivCortex2Client
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "BCI"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# ============================================================================================
url = "wss://localhost:6868"
emotive = None
profile_name = "FakeBCI"
CLIENT_ID = "bhOr0ZmsLWZVDeFl0QHE08e05lDI36blefUxfbLX"
CLIENT_SECRET = "BL3OlfhwzzPMXcxgFYT7uxaB6LSEAlwdLfqU4OG2oRJkRbQg63h4KMpvNp3144pOsybUpNLDrPQXuDXRC18oyIQUxh6Jum9ktR3nTNwChLW1ZdCcpzcuaavycLD000wK"
# ===========================================
txt_rl1 = "1"
# =====================Arduino===============================


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
    emotive.subscribe(streams=["com"])
    emotive.mental_command_action_sensitivity("get", profile_name)
    # print(emotive.create_record("FakeRecord"))


def connect_mqtt():
    connect_cortexAPI()
    get_com_emotiv()
    # record()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    global emotive
    msg_count = 0
    result = ""
    while True:
        emotive.mental_command_action_sensitivity("get", profile_name)
        data = emotive.receive_data()["com"]
        txt = input()
        msg = f"[{txt}]"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send : {msg} => ({topic})")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


def catch_event(msg):
    if(msg == "[user]"):
        print(CortexAPI.get_user_login())
    # elif(msg == "[]"):
        # print()


if __name__ == '__main__':
    run()
