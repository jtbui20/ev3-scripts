#!/usr/bin/env python3
# Import the motors we're going to be using
from typing import List
import math

from .Motors import default_motor_configuration
from .MotorModule import MotorModule
from .helpers import RadialMove, RadialTurn, AddMatrix


class OmniWheelMotorModule(MotorModule):
    """Class that defines how an omni wheel robot should move."""

    def __init__(self, motor_configuration=default_motor_configuration, debug=False):
        super().__init__(motor_configuration=default_motor_configuration, debug=debug)

    def RadialMove(
        self,
        angle,
        speed=100,
        motor_order_offset=1,
    ):
        """Takes an angle that you want to travel in and sets motor values to it"""
        values = RadialMove(
            angle, speed, motor_count=4, motor_order_offset=motor_order_offset
        )

        if self.debug:
            print(values)

        self.finalMotorValues = AddMatrix(self.finalMotorValues, values)
        return values

    def RadialTurn(self, currentAngle, targetAngle, spread=30, speed=10):
        """Takes an angle that you want to turn towards and sets motor values to it"""
        values = RadialTurn(currentAngle, targetAngle, spread, speed)

        if self.debug:
            print(values)

        self.finalMotorValues = AddMatrix(self.finalMotorValues, values)
        return values
