#!/usr/bin/env python3
import math, time
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor import Sensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.button import Button

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

def RadialMove( angle, speed = 100):
    # Convert angle from degrees to radian
    theta = math.radians(angle);
    # Build an array of the values
    values = [0, 0, 0, 0]
    for i in range(0, 4):
      values[i] = math.sin(theta - (i * math.pi / 2) - math.pi / 4)
      # Round to make it easier to work with
      values[i] = round(values[i], 4)
    
    # Amp it up to the speed that we want
    amp_ratio = speed/ max(values)
    values = [amp_ratio * x for x in values]
    for i in range(0, 4):
      values[i] = min(100, max(-100, values[i]))

    # Now we assign it to the motors
    m_fl.on(-values[0])
    m_fr.on(-values[1])
    m_br.on(-values[2])
    m_bl.on(-values[3])

def StopMotor():
  m_fl.off()
  m_fr.off()
  m_br.off()
  m_bl.off()

prev = 0
def MoveToBall(val):
    if val in [1,2,3]: RadialMove(-90,50)
    elif val in [4,5,6]: RadialMove(0,50)
    elif val in [7,8,9]: RadialMove(90,50)
    else: RadialMove(180,50)

state = False
button = Button()
while True:
  if button.enter:
    state = (not state)
    print(state)
    time.sleep(1)
  if state:
    irv = irs.value(0)
    ang = cps.value(0)
    usv = us.distance_centimeters
    
    MoveToBall(irv)
  else:
    StopMotor()