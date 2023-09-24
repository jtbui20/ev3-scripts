#!/usr/bin/env python3

# We're going to be doing a ton of math
import time

# Ev3sim dependency
from ev3sim.code_helpers import wait_for_tick, is_sim, format_print

# Make a robot object and assign it some stuff
from robots.BaseRobot.Base_Robot import Base_Robot
from robots.BaseRobot.Motors.helpers import AngleBetween


if __name__ == "__main__":
    robot = Base_Robot(Simulator=is_sim, Debug=False)

    rootDir = robot.cp.value(0)
    state = False

    while True:
        if not is_sim:
            if robot.button.enter:
                state = not state
                if state:
                    rootDir = robot.cp.value(0)
                time.sleep(1)
        else:
            state = True

        if state:
            robot.motors.ResetMotorValues()
            # Grab sensor values
            cp = robot.cp.value(0)
            ir = robot.ir.value(0)

            # Logic stuff here
            dir = 0
            if ir in [1, 2, 3]:
                dir = -90
            elif ir in [4, 5, 6]:
                dir = 0
            elif ir in [7, 8, 9]:
                dir = 90
            else:
                dir = 180

            # Assign movement
            robot.motors.RadialMove(dir, speed=100)
            motorVals = robot.motors.RadialTurn(cp, rootDir, spread=10)
            robot.motors.RunMotors(speed=100)
            if robot.Simulator:
                wait_for_tick()
        else:
            robot.motors.StopMotors()
