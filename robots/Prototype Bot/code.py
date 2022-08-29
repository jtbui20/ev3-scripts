#!/usr/bin/env 3

# Import the motors we're going to be using
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
# Import the sensors we're going to be using
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
# We're going to be doing a ton of math
import math
import numpy as np
import time
# Ev3sim dependency
from ev3sim.code_helpers import wait_for_tick

# Make a robot object and assign it some stuff
from BaseRobot.Base_Robot import Base_Robot

class Robot(Base_Robot):
  pass

if __name__ == "__main__":
  R = Robot(Brick=True, Debug=False)
  while True:
    print(R.USonH.value(), R.USonH.value())
    time.sleep(1)