from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
from cortex2 import EmotivCortex2Client
from paho.mqtt import client as mqtt_client

hostName = "localhost"
serverPort = 8080
lc = "utf-8"
# =========================================================================
url = "wss://localhost:6868"
emotive = None
profile_name = "FakeBCI"
CLIENT_ID = "bhOr0ZmsLWZVDeFl0QHE08e05lDI36blefUxfbLX"
CLIENT_SECRET = "BL3OlfhwzzPMXcxgFYT7uxaB6LSEAlwdLfqU4OG2oRJkRbQg63h4KMpvNp3144pOsybUpNLDrPQXuDXRC18oyIQUxh6Jum9ktR3nTNwChLW1ZdCcpzcuaavycLD000wK"
STREAM = "com"
# =============================================================================


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

# =========================================================================


def add_element(s, str):
    s.wfile.write(bytes(str, lc))


class KHKT_BCI(BaseHTTPRequestHandler):
    def do_GET(seft):

        seft.send_response(200)
        seft.send_header("Content-type", "text/html")
        seft.end_headers()
        add_element(seft, "<html><head><title>BCI_KHKT</title></head>")
        add_element(seft, "<body>")
        add_element(seft, "<p style='font-size:35px;'>hello world</p>")
        add_element(seft, "</body></html>")


if __name__ == "__main__":
    server = HTTPServer((hostName, serverPort), KHKT_BCI)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")
