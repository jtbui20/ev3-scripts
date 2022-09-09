#!/usr/bin/env python3
import math
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor import Sensor
from ev3dev2.sensor.lego import UltrasonicSensor

print("Test")
# IR sensor
irs = Sensor("in3", driver_name="ht-nxt-ir-seek-v2")
irs.mode = "AC-ALL"
# Ultrasonic sensor to cm
us = UltrasonicSensor("in1")
us.mode = us.MODE_US_DIST_CM
# Compass sensor to default
cps = Sensor("in2", driver_name="ht-nxt-compass")
cps.command = 'BEGIN-CAL'
cps.command = 'END-CAL'

m_bl = LargeMotor("outA")
m_fl = LargeMotor("outB")
m_fr = LargeMotor("outC")
m_br = LargeMotor("outD")
prev = 0

while True:
  m_bl.on(100)
  m_fl.on(100)
  m_fr.on(100)
  m_br.on(100)