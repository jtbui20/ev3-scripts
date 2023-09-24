from ev3dev2.motor import (
    Motor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
)
from time import sleep

default_motor_configuration = [
    {"Port": OUTPUT_A},
    {"Port": OUTPUT_B},
    {"Port": OUTPUT_C},
    {"Port": OUTPUT_D},
]


class EV3Motor:
    def __init__(self, config):
        self.port = config.get("Port", None)
        self.__motor = None  # type: Motor
        self.__error = False

        self.CreateMotorAdapter()

    def CreateMotorAdapter(self):
        try:
            self.__motor = Motor(self.port)
            self.__motor.stop_action = self.__motor.STOP_ACTION_HOLD
            return self
        except Exception as e:
            raise e

    def HandleErrorStop(self):
        try:
            self.Off(True)
        except:
            self.__error = True
            print("Motor {port} has disconnected".format(port=self.port))

            while self.__error:
                try:
                    self.CreateMotorAdapter()
                    self.__error = False
                except Exception as e:
                    print("Please reconnect motor {port}".format(port=self.port))
                    sleep(1)
                    continue

    def On(self, speed):
        self.__motor.on(speed)

    def Off(self, mode):
        mode = True if mode in [1, "BRAKE", True] else False
        self.__motor.stop()

    @property
    def isStalled(self):
        return self.__motor.is_stalled
