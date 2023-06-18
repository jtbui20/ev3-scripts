#!/usr/bin/env python3
# Import the motors we're going to be using
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, Motor
from typing import List
from collections.abc import Callable
import math

default_motor_configuration = [
  (OUTPUT_A, LargeMotor),
  (OUTPUT_B, LargeMotor),
  (OUTPUT_C, LargeMotor),
  (OUTPUT_D, LargeMotor)
]

'''Master class for motor related actions.'''
class OmniWheelMotorModule:
  def __init__(self, motor_configuration = default_motor_configuration, debug = False):
    self.motorReferences: List[Motor] = []
    for port, motorType in motor_configuration:
      self.motorReferences.append(motorType(port))

    self.debugMode = debug
    self.finalValues = [0, 0, 0, 0]

    if self.debugMode: print("Motors are online")

  @staticmethod
  def AddMatrix(A, B):
    return [A[i] + B[i] for i in range(0, len(A))]

  def BindGetNorth(self, func: Callable[[None], int]):
    self.getNorthValue = func
  
  '''Takes an angle that you want to travel in and sets motor values to it'''
  def RadialMove(self, angle: int, speed: int = 100, motor_order_offset: int = 1, relativeToField = False) -> List[int]:
    values = [0, 0, 0, 0]
    # If speed is 0, set values to 0
    if speed != 0:
      if self.getNorthValue and relativeToField:
        angle = angle + self.getNorthValue()

      theta = math.radians(angle)
      values = [math.sin(theta - ((i + motor_order_offset) * math.pi / 2) - math.pi / 4) for i in range(0, 4)]

      values = self.ClampSpeed(values, speed)
    
    if self.debugMode: print(values)

    self.finalValues = self.AddMatrix(self.finalValues, values)
    return values

  '''Takes an angle that you want to turn towards and sets motor values to it'''
  def RadialTurn(self, currentAngle: int, targetAngle: int, spread: int = 30, speed: int = 10) -> List[int]:
    differenceAngle = self.AngleBetween(currentAngle, targetAngle)

    values = [0, 0, 0, 0]
    if differenceAngle < -spread:
      values = [speed, 0, speed, 0]
    elif spread < differenceAngle:
      values = [0, -speed, 0, -speed]
    else:
      values = [0, 0, 0, 0]

    if self.debugMode: print(values)

    self.finalValues = self.AddMatrix(self.finalValues, values)
    return values

  def RadialFieldTurn(self, targetAngle: int, spread: int = 30, speed: int = 10) -> List[int]:
    if self.getNorthValue:
      return self.RadialTurn(self.getNorthValue(), targetAngle,spread, speed)
    else:
      return [0, 0, 0, 0]
  
  def RunMotors(self, speed = 100):
    self.finalValues = self.ClampSpeed(self.finalValues, speed)
    for motor, value in zip(self.motorReferences, self.finalValues):
      motor.off() if value == 0 else motor.on(SpeedPercent(value))
    self.finalValues = [0, 0, 0, 0]
  
  def StopMotors(self):
    for motor in self.motorReferences:
      motor.off()
    self.finalValues = [0, 0, 0, 0]

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