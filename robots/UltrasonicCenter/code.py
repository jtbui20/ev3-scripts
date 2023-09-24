#!/usr/bin/env python3

from time import sleep
from robots.BaseRobot.Base_Robot import Base_Robot
import threading

# Goal Area : 50cm - 97cm
# Mid: 73cm
# Normal Backwall: 27cm
# Goal Backwall: 4cm
# White Line: 14cm

# 14 - 50 -73 - 97

# Left lean (ang = 0, top wall)
# w = wall, h = back

# Right lean (ang = 90, bottom wall)
# w = back, h = wall


class Robot(Base_Robot):
    def __init__(self, Simulator=True, Debug=True):
        super().__init__(Simulator, Debug)

        self.rootDir = self.cp.value(0)
        self.forwardDir = self.rootDir
        self.facingTop = True
        self.facingReady = True

        self.mid = self.us_w.value(0)

    def Input(self):
        self.w_v = self.us_w.value(0)
        self.h_v = self.us_h.value(0)
        self.cp_v = self.cp.value(0)
        self.ir_v = self.ir.value(0)

    def Process(self):
        self.sideWall = self.w_v if (self.facingTop) else self.h_v
        self.backWall = self.h_v if (self.facingTop) else self.w_v

        self.forwardDir = self.rootDir if (self.facingTop) else self.rootDir + 90

        if self.sideWall > self.mid + 10 and False:
            print(self.facingReady, self.facingTop)
            if self.facingReady:
                self.facingTop = not self.facingTop
                threading.Thread(target=self.HangReady).start()

    def Output(self):
        dir = 0
        if self.ir_v in [1, 2, 3]:
            dir = -90
        elif self.ir_v in [4, 5, 6]:
            dir = 0
        elif self.ir_v in [7, 8, 9]:
            dir = 90
        else:
            dir = 180

        if dir == 180:
            self.motors.RadialMove(dir, speed=100)
        else:
            self.motors.RadialMove(dir, speed=100)

        # Horizontal movement
        if self.sideWall < 14:
            wallDir = 90 if (self.facingTop) else -90
            self.motors.RadialMove(wallDir)

        # Move forwards away from corners
        if (50 <= self.sideWall) and (self.sideWall <= 97):
            if self.backWall < 1:
                R.motors.RadialMove(0)
        elif (self.sideWall < 50) or (97 < self.sideWall):
            if self.backWall < 20:
                R.motors.RadialMove(0)

        # Directional rotation
        R.motors.RadialTurn(self.cp_v, self.forwardDir, spread=22, speed=100)
        # Move towards ball

        self.motors.RunMotors()

    def HangReady(self):
        self.facingReady = False
        sleep(1)
        self.facingReady = True


if __name__ == "__main__":
    R = Robot(Simulator=True, Debug=False)
    if R.Simulator:
        from ev3sim.code_helpers import wait_for_tick

    while True:
        R.Input()
        R.Process()
        R.Output()

        sleep(0.1)
