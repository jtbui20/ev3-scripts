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
  def __init__(self, Simulator = False, Debug = False):
    self.Simulator = Simulator
    self.Debug = Debug

    # These are fields for our output motors
    self._OA = LargeMotor(OUTPUT_A);
    self._OB = LargeMotor(OUTPUT_B);
    self._OC = LargeMotor(OUTPUT_C);
    self._OD = LargeMotor(OUTPUT_D);

    if Debug: print("Motors are online")

    # These are fields for our input sensors
    self.us_w = UltrasonicSensor(INPUT_1);
    self.us_w.mode = self.us_w.MODE_US_DIST_CM
    self.us_h = UltrasonicSensor(INPUT_4);
    self.us_h.mode = self.us_h.MODE_US_DIST_CM
    self.cp = Sensor(INPUT_2, driver_name="ht-nxt-compass")
    self.ir = Sensor(INPUT_3, driver_name="ht-nxt-ir-seek-v2")
    self.ir.mode = "AC-ALL"
    # Only make if not simulator
    if not self.Simulator:
      self.button = Button()
      self.sound = Sound()

    if Debug: print("Sensors are online")

  def PlaySound_Boot(self):
    if self.Simulator: return
    self.sound.play_song(
      [('C4', 'q'), ('E4', 'q'), ('G4', 'q')], tempo=240
    )
  def PlaySound_Stop(self):
    if self.Simulator: return
    self.sound.play_song(
      [('G4', 'q'), ('E4', 'q'), ('C4', 'q')], tempo=240
    )

  '''Calibration Process'''
  def Calibrate(self, length):
    self.cp.command("BEGIN-CAL")
    time.sleep(length)
    self.cp.command("END-CAL")

  '''Takes an input angle and moves in that direction'''
  def RadialMove(self, angle, speed = 100):
    # Convert angle from degrees to radian
    theta = math.radians(angle);
    # Build an array of the values
    values = [0, 0, 0, 0]
    for i in range(0, 4):
      values[i] = math.sin(theta - ((i + 1) * math.pi / 2) - math.pi / 4)
      # Round to make it easier to work with
      values[i] = round(values[i], 4)
    
    # Amp it up to the speed that we want
    amp_ratio = speed/ max(values)
    values = [amp_ratio * x for x in values]
    values = [min(100, max(-100, x)) for x in values]

    if self.Debug:
      print(values)
    
    return values

  def RadialTurn(self, currentAngle, targetAngle, range = 10, speed = 100):
    target= math.radians(targetAngle)
    rangeDiff = math.radians(range)
    targets = [target - rangeDiff, target + rangeDiff]
    current = math.radians(currentAngle)

  def AssignMotors(self, values):
    self._OA.on(values[0])
    self._OB.on(values[1])
    self._OC.on(values[2])
    self._OD.on(values[3])

  def Stop(self):
    self.AssignMotors([0,0,0,0])