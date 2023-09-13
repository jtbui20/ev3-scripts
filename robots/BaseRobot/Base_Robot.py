#!/usr/bin/env python3

# Import the motors we're going to be using
# Import the sensors we're going to be using
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.button import Button
# We're going to be doing a ton of math
import time

from BaseRobot.Motors import OmniWheelMotorModule
from BaseRobot.SoundModule import SoundModule

class Base_Robot:
  def __init__(self, Simulator = False, Debug = False):
    self.Simulator = Simulator
    self.Debug = Debug

    # These are fields for our output motors
    self.motors = OmniWheelMotorModule(debug=Debug)

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
      self.sound = SoundModule(Simulator= self.Simulator)

    if Debug: print("Sensors are online")

    self.motors.BindGetNorth(lambda: self.cp.value(0))
  
  def GenerateSounds(self):
    self.sound.NewPattern("Boot",
      [('C4', 'q'), ('E4', 'q'), ('G4', 'q')], tempo=240
    )

    self.sound.NewPattern("Stop",
      [('G4', 'q'), ('E4', 'q'), ('C4', 'q')], tempo=240
    )

  def PlaySound_Boot(self):
    if self.Simulator: return
    self.sound.PlaySound("Boot")

  def PlaySound_Stop(self):
    if self.Simulator: return
    self.sound.PlaySound("Stop")

  '''Calibration Process'''
  def Calibrate(self, length):
    self.cp.command = "BEGIN-CAL"
    time.sleep(length)
    self.cp.command ="END-CAL"