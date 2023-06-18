#!/usr/bin/env python3

# We're going to be doing a ton of math
import math
import time
# Ev3sim dependency
from ev3sim.code_helpers import wait_for_tick, is_ev3, is_sim

# Make a robot object and assign it some stuff
from robots.BaseRobot.Base_Robot import Base_Robot

class Robot(Base_Robot):
  pass

def AddMatrix(A, B):
  return [A[i] + B[i] for i in range(0, len(A))]

if __name__ == "__main__":
  robot = Robot(Simulator=is_sim, Debug=False)
  
  # Calibrate values
  # R.Calibrate(0.5)
  # Root direction is the initial reading
  rootDir = robot.cp.value(0)

  robot.motors.BindGetNorth(lambda: robot.cp.value(0))

  # Do boot up tone
  robot.PlaySound_Boot()

  state = False

  while True:
    if (not is_sim):
      if (robot.button.enter):
        state = not state
        if (state): 
          robot.PlaySound_Boot()
          rootDir = robot.cp.value(0)
        else: robot.PlaySound_Stop()
        time.sleep(1)
    else:
      state = True
    
    if state:
      # Grab sensor values
      cp = robot.cp.value(0)
      ir = robot.ir.value(0)
      us_w = robot.us_w.distance_centimeters
      us_h = robot.us_h.distance_centimeters

      # Logic stuff here
      dir = 0
      if ir in [1,2,3]: dir = -90
      elif ir in [4,5,6]: dir = 0
      elif ir in [7,8,9]: dir = 90
      else: dir = 180

      # Assign movement
      robot.motors.RadialMove(dir, speed = 100)
      robot.motors.RunMotors()
      if (robot.Simulator): wait_for_tick()
    else:
      robot.Stop()