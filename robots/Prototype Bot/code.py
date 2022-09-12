#!/usr/bin/env python3

# We're going to be doing a ton of math
import math
import time
# Ev3sim dependency
# from ev3sim.code_helpers import wait_for_tick

# Make a robot object and assign it some stuff
from Base_Robot import Base_Robot

class Robot(Base_Robot):
  pass

def AddMatrix(A, B):
  return [A[i] + B[i] for i in range(0, len(A))]

if __name__ == "__main__":
  R = Robot(Simulator=False, Debug=False)
  
  
  # Calibrate values
  # R.Calibrate(0.5)
  # Root direction is the initial reading
  rootDir = R.cp.value(0)

  # Do boot up tone
  R.PlaySound_Boot()

  state = False
  if R.Simulator:
    from ev3sim.code_helpers import wait_for_tick
  while True:
    if (not R.Simulator):
      if (R.button.enter):
        state = not state
        if (state): 
          R.PlaySound_Boot()
          rootDir = R.cp.value(0)
        else: R.PlaySound_Stop()
        time.sleep(1)
    else:
      state = True
    
    if state:
      # Grab sensor values
      cp = R.cp.value(0)
      ir = R.ir.value(0)
      us_w = R.us_w.distance_centimeters
      us_h = R.us_h.distance_centimeters

      # Logic stuff here
      dir = 0
      if ir in [1,2,3]: dir = -90
      elif ir in [4,5,6]: dir = 0
      elif ir in [7,8,9]: dir = 90
      else: dir = 180

      # Assign movement
      # values = R.RadialMove(dir)
      values = [0,0,0,0]
      turn = R.RadialTurn(cp, rootDir, rootDir, spread = 20, speed = 100)
      values = AddMatrix(values, turn)
      values = R.ClampSpeed(values, 100)
      R.AssignMotors(values)
      if (R.Simulator): wait_for_tick()
    else:
      R.Stop()