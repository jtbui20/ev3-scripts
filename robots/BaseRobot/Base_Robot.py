#!/usr/bin/env python3

# Import the motors we're going to be using
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
# Import the sensors we're going to be using
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
# We're going to be doing a ton of math
import math, time

import threading

class Base_Robot:
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

    if Debug: print("Motors are online")

    # These are fields for our input sensors
    self.USonW = UltrasonicSensor(INPUT_1);
    self.USonW.mode = self.USonW.MODE_US_DIST_CM
    self.USonH = UltrasonicSensor(INPUT_4);
    self.USonH.mode = self.USonH.MODE_US_DIST_CM
    self.CPSen = Sensor(INPUT_2, driver_name="ht-nxt-compass")
    self.IRSen = Sensor(INPUT_3, driver_name="ht-nxt-ir-seek-v2")
    self.IRSen.mode = "AC-ALL"
    self.button = Button()
    self.sound = Sound()

    if Debug: print("Sensors are online")

  def PlaySound_Boot(self):
    self.sound.play_song(
      [('C4', 'q'), ('E4', 'q'), ('G4', 'q')]
    )
  def PlaySound_Stop(self):
    self.sound.play_song(
      [('G4', 'q'), ('E4', 'q'), ('C4', 'q')]
    )

  '''Calibration Process'''
  def Calibrate(self, length):
    self.CPSen.command("BEGIN-CAL")
    time.sleep(length)
    self.CPSen.command("END-CAL")

  '''Takes an input angle and moves in that direction'''
  def RadialMove(self, angle, speed = 100):
    # Convert angle from degrees to radian
    theta = math.radians(angle);
    # Build an array of the values
    values = [0, 0, 0, 0]
    for i in range(0, 4):
      values[i] = math.sin(theta - (((2 * i ) + 1) * math.pi / 4))
      # Round to make it easier to work with
      values[i] = round(values[i], 4)
    
    # Amp it up to the speed that we want
    amp_ratio = speed/ max(values)
    values = [amp_ratio * x for x in values]
    values = [min(100, max(-100, x)) for x in values]

    if self.Debug:
      print(values)

    # Now we assign it to the motors
    if self.hasBrick:
      self._OA.on(-values[0])
      self._OB.on(-values[1])
      self._OC.on(-values[2])
      self._OD.on(-values[3])

  def Stop(self):
    self._OD.off()  
    self._OC.off()
    self._OB.off()
    self._OA.off()