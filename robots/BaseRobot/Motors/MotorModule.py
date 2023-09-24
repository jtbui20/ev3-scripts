from ev3dev2.motor import (
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
)

from .helpers import ClampSpeed
from .Motors import EV3Motor

default_motor_configuration = [
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
]


class MotorModule:
    """Master class for motor related actions."""

    def __init__(self, motor_configuration=[], debug=False):
        self.motorReferences = []  # type: list[EV3Motor]
        self.motorPorts = []
        for entry in motor_configuration:
            try:
                m = EV3Motor(entry)
                self.motorPorts.append(m.port)
                self.motorReferences.append(m)
            except Exception as e:
                # raise Exception(
                #     "Error initializing motor on port {port}: {error}".format(
                #         port=port, error=e
                #     )
                # )
                raise e

        self.defaultMotorValues = [float(0)] * len(self.motorReferences)

        self.finalMotorValues = self.defaultMotorValues
        self.debug = debug

        if self.debug:
            print("Base Motor Modules are online.")

    def ResetMotorValues(self):
        """Sets all motors to run at 0 speed"""
        self.finalMotorValues = self.defaultMotorValues

    def __HandleInterrupt(function):  # type: ignore
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)  # type: ignore
            except Exception as e:
                for key, motor in enumerate(self.motorReferences):
                    motor.HandleErrorStop()
                    self.finalMotorValues[key] = 0

        return wrapper

    @__HandleInterrupt
    def isStalled(self):
        """Returns True if any of the motors are stalled"""
        return any([motor.isStalled for motor in self.motorReferences])

    @__HandleInterrupt
    def RunMotors(self, speed=100):
        """Runs the output motors of computed values to the motors"""
        self.finalMotorValues = ClampSpeed(self.finalMotorValues, speed)
        for motor, value in zip(self.motorReferences, self.finalMotorValues):
            motor.Off("brake") if value == 0 else motor.On(value)

        if self.debug:
            print(
                "Running motors at {motorValues}".format(
                    motorValues=self.finalMotorValues
                )
            )

    @__HandleInterrupt
    def StopMotors(self):
        for motor in self.motorReferences:
            motor.Off("brake")

        self.ResetMotorValues()
