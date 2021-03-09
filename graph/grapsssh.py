# importing libraries
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation
import random
import time
from matplotlib.lines import Line2D
from cortex2 import EmotivCortex2Client
from paho.mqtt import client as mqtt_client
# ===================================================================
url = "wss://localhost:6868"
emotive = None
profile_name = "FakeBCI"
CLIENT_ID = "bhOr0ZmsLWZVDeFl0QHE08e05lDI36blefUxfbLX"
CLIENT_SECRET = "BL3OlfhwzzPMXcxgFYT7uxaB6LSEAlwdLfqU4OG2oRJkRbQg63h4KMpvNp3144pOsybUpNLDrPQXuDXRC18oyIQUxh6Jum9ktR3nTNwChLW1ZdCcpzcuaavycLD000wK"
STREAM = "com"
# =====================================================================


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


class Scope:
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 1.1)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def getData():
    return 0


def emitter(p=0.1):
    """Return a random value in [0, 1) with probability p, else 0."""
    while True:
        emotive.mental_command_action_sensitivity("get", profile_name)
        data = emotive.receive_data()[STREAM][1]
        yield data


connect_cortexAPI()
get_com_emotiv()

np.random.seed(19680801 // 10)


fig, ax = plt.subplots()
# fig, ax = plt.subplots(2, 2)
# scope1 = Scope(ax[0][0])
scope1 = Scope(ax)
ani1 = animation.FuncAnimation(fig, scope1.update, emitter, interval=200,
                               blit=True)

# scope2 = Scope(ax[0][1])
# ani2 = animation.FuncAnimation(fig, scope2.update, emitter, interval=1,
#                                blit=True)
# scope3 = Scope(ax[1][0])
# ani3 = animation.FuncAnimation(fig, scope3.update, emitter, interval=1,
#                                blit=True)
# scope4 = Scope(ax[1][1])
# ani4 = animation.FuncAnimation(fig, scope4.update, emitter, interval=1,
#                                blit=True)
plt.show()
