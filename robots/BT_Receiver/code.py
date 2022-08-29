#!/usr/bin/env 3

# We're going to be doing a ton of math
import math
import numpy as np
import time
# Ev3sim dependency
from ev3sim.code_helpers import wait_for_tick
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
# Make a robot object and assign it some stuff
from BaseRobot.Base_Robot import Base_Robot

class Receiver(Base_Robot):
  def __init__(self, target_connection):
    self.__init__()

    if self.hasBrick:
      self.client = BluetoothMailboxClient
      self.mbox = TextMailbox("MainBox", self.client)

      self.client.connect(target_connection)

if __name__ == "__main__":
  R = Receiver("bot0")
  print(R.mbox.wait_new())