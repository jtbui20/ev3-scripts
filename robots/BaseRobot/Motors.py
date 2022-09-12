#!/usr/bin/env python3
# Import the motors we're going to be using
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, Motor
from typing import List
import math

'''Master class for motor related actions.'''
class MotorModule:
  def __init__(self, order = [OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D], type = [LargeMotor, LargeMotor, LargeMotor, LargeMotor], debug = False):
    self.motorArray: List[Motor] = []
    for motor, port in zip(type, order):
      self.motorArray.append(motor(port))

    self.debug = debug
    self.values = [0, 0, 0, 0]
    if debug: print("Motors are online")

  @staticmethod
  def AddMatrix(A, B):
    return [A[i] + B[i] for i in range(0, len(A))]

  '''Takes an angle that you want to travel in and sets motor values to it'''
  def RadialMove(self, angle: int, speed: int, offset: int = 1) -> List[int]:
    
    values = [0, 0, 0, 0]
    # If speed is 0, set values to 0
    if speed != 0:
      # Convert to radians for trig functions
      theta = math.radians(angle)
      # Return array
      values = [math.sin(theta - ((i + offset) * math.pi / 2) - math.pi / 4) for i in range(0, 4)]

      # Limit to motor min max
      values = self.ClampSpeed(values, speed)
    
    if self.debug: print(values)

    self.values = self.AddMatrix(self.values, values)
    return values

  '''Takes an angle that you want to turn towards and sets motor values to it'''
  def RadialTurn(self, currentAngle: int, referenceAngle: int, spread: int = 30, speed: int = 10) -> List[int]:
    differenceAngle = self.AngleBetween(currentAngle, referenceAngle)

    values = [0, 0, 0, 0]
    if differenceAngle < -spread:
      values = [speed, 0, speed, 0]
    elif spread < differenceAngle:
      values = [0, -speed, 0, -speed]
    else:
      values = [0, 0, 0, 0]

    if self.debug: print(values)

    self.values = self.AddMatrix(self.values, values)
    return values
  
  def RunMotors(self, speed = 100):
    self.values = self.ClampSpeed(self.values, speed)
    for motor, value in zip(self.motorArray, self.values):
      motor.off() if value == 0 else motor.on(SpeedPercent(value))
  
  def StopMotors(self):
    for motor in self.motorArray:
      motor.off()

  '''Maximizes the set of values to a desired quantity while maintaining ration, and limits between -100 and 100'''
  @staticmethod
  def ClampSpeed(values: List[int], speed: int = 100) -> List[int]:
    high = max([abs(x) for x in values])
    if high == 0: return values
    ratio = speed / high
    return [min(100, max(-100, ratio * x)) for x in values]

  '''Gets the difference between two directions'''
  @staticmethod
  def AngleBetween(current: int, target: int):
    return ((current - target + 180) % 360) - 180