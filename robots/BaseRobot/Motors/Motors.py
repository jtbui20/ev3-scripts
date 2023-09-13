from ev3dev2.motor import (
    LargeMotor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
    SpeedPercent,
    Motor,
)
from typing import List

default_motor_configuration = [
    (OUTPUT_A, LargeMotor),
    (OUTPUT_B, LargeMotor),
    (OUTPUT_C, LargeMotor),
    (OUTPUT_D, LargeMotor),
]

class MotorModule:
    """Master class for motor related actions."""

    def __init__(self, motor_configuration=default_motor_configuration, debug=False):
        self.motorReferences: List[Motor] = []
        for port, motorType in motor_configuration:
            self.motorReferences.append(motorType(port))

        self.debugMode = debug
        self.finalValues = [0, 0, 0, 0]

        if self.debugMode:
            print("Motors are online")

    @staticmethod
    def AddMatrix(A, B):
        return [A[i] + B[i] for i in range(0, len(A))]

    def RunMotors(self, speed=100):
        """Runs the output of computed values to the motors"""
        self.finalValues = self.ClampSpeed(self.finalValues, speed)
        for motor, value in zip(self.motorReferences, self.finalValues):
            motor.off() if value == 0 else motor.on(SpeedPercent(value))
        self.finalValues = [0, 0, 0, 0]

    def StopMotors(self):
        """Turns off all motors and sets the final values to 0"""
        for motor in self.motorReferences:
            motor.off()
        self.finalValues = [0, 0, 0, 0]

    @staticmethod
    def ClampSpeed(values: List[int], speed: int = 100) -> List[int]:
        """Changes the highest motor speed to the speed specified while maintaining the ratio of the other motors"""
        high = max([abs(x) for x in values])
        if high == 0:
            return values
        ratio = speed / high
        return [min(100, max(-100, ratio * x)) for x in values]
