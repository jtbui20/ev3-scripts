#!/usr/bin/env 3

# We're going to be doing a ton of math
import math
import numpy as np
import time
# Ev3sim dependency
# from ev3sim.code_helpers import wait_for_tick

# Make a robot object and assign it some stuff
from BaseRobot.Base_Robot import Base_Robot

class Robot(Base_Robot):
  pass

if __name__ == "__main__":
  R = Robot(Brick=True, Debug=True)