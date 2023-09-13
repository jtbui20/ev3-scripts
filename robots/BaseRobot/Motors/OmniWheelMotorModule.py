#!/usr/bin/env python3
# Import the motors we're going to be using
from typing import List
import math

from Motors import MotorModule, default_motor_configuration

class OmniWheelMotorModule(MotorModule):
    """Class that defines how an omni wheel robot should move."""

    def __init__(self, motor_configuration=default_motor_configuration, debug=False):
        super().__init__(motor_configuration, debug)

    def RadialMove(
        self,
        angle: int,
        speed: int = 100,
        motor_order_offset: int = 1,
    ) -> List[int]:
        """Takes an angle that you want to travel in and sets motor values to it"""
        values = [0, 0, 0, 0]
        # If speed is 0, set values to 0
        if speed != 0:
            theta = math.radians(angle)
            values = [
                math.sin(theta - ((i + motor_order_offset) * math.pi / 2) - math.pi / 4)
                for i in range(0, 4)
            ]

            values = self.ClampSpeed(values, speed)

        if self.debugMode:
            print(values)

        self.finalValues = self.AddMatrix(self.finalValues, values)
        return values

    def RadialTurn(
        self, currentAngle: int, targetAngle: int, spread: int = 30, speed: int = 10
    ) -> List[int]:
        """Takes an angle that you want to turn towards and sets motor values to it"""
        differenceAngle = self.AngleBetween(currentAngle, targetAngle)

        values = [0, 0, 0, 0]
        if differenceAngle < -spread:
            values = [speed, 0, speed, 0]
        elif spread < differenceAngle:
            values = [0, -speed, 0, -speed]
        else:
            values = [0, 0, 0, 0]

        if self.debugMode:
            print(values)

        self.finalValues = self.AddMatrix(self.finalValues, values)
        return values

    @staticmethod
    def AngleBetween(current: int, target: int) -> (int, int):
        """Gets the difference between two directions"""
        angle_dif = ((current - target + 180) % 360) - 180
        direction = 1 if (angle_dif > 0) else -1
        return (abs(angle_dif), direction)
