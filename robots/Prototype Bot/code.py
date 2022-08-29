#!/usr/bin/env 3

# Import the motors we're going to be using
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
# Import the sensors we're going to be using
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
# We're going to be doing a ton of math
import math
import numpy as np
# More math!
from bezier import Bezier, Progression

import time
# Ev3sim dependency
from ev3sim.code_helpers import wait_for_tick, CommandSystem
# Make a robot object and assign it some stuff


class Robot:
  def __init__(self, Brick = False, Debug = False):
    self.hasBrick = Brick
    self.Debug = Debug
    # If we don't have a brick, don't do brick associated stuff
    if not Brick:
      return

    # These are fields for our output motors
    self._OA = LargeMotor(OUTPUT_A);
    self._OB = LargeMotor(OUTPUT_B);
    self._OC = LargeMotor(OUTPUT_C);
    self._OD = LargeMotor(OUTPUT_D);

    if self.Debug:
      print("Motors are online")

    # These are fields for our input sensors
    self.USonW = UltrasonicSensor(INPUT_1);
    self.USonW.mode = self.USonW.MODE_US_DIST_CM
    self.USonH = UltrasonicSensor(INPUT_4);
    self.USonH.mode = self.USonH.MODE_US_DIST_CM
    self.IRSen = Sensor(INPUT_3, driver_name="ht-nxt-ir-seek-v2")
    self.IRSen.mode = "AC-ALL"

    if Debug:
      print("Sensors are online")

  '''Takes an input angle and moves in that direction'''
  def RadialMove(self, angle, speed = 100):
    # Convert angle from degrees to radian
    theta = math.radians(angle);
    # Build an array of the values
    values = [0, 0, 0, 0]
    for i in range(0, 4):
      values[i] = math.cos(theta + (((2 * i ) + 1) * math.pi / 4))
      # Round to make it easier to work with
      values[i] = round(values[i], 4)
    
    # Amp it up to the speed that we want
    amp_ratio = speed/ max(values)
    values = [amp_ratio * x for x in values]
    values = np.clip(values, -100, 100)

    if self.Debug:
      print(values)

    # Now we assign it to the motors
    if self.hasBrick:
      self._OA.on(values[0])
      self._OB.on(values[1])
      self._OC.on(values[2])
      self._OD.on(values[3])

  def Stop(self):
    self._OD.off()  
    self._OC.off()
    self._OB.off()
    self._OA.off()


if __name__ == "__main__":
  R = Robot(Brick=True, Debug=False);
  # Generate a path that we want to follow
  points = np.array([
    (0,0),
    (-0.8,3),
    (1,0),
    (1,1)
  ])
  path = Bezier.Curve(np.linspace(0,1,31), points)
  angles = Progression(path)

  for i in angles:
    R.RadialMove(i)
    wait_for_tick()
  R.Stop()
  