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

from Motors import MotorModule;

class Base_Robot:
  def __init__(self, Simulator = False, Debug = False):
    self.Simulator = Simulator
    self.Debug = Debug

    # These are fields for our output motors
    self.motors = MotorModule()

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
      self.sound.set_volume(5)

    if Debug: print("Sensors are online")

    self.motors.BindCompass(self.cp)

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