import time
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3sim.code_helpers import CommandSystem

leftMotor = LargeMotor("outA")
rightMotor = LargeMotor("outB")
color = ColorSensor("in1")
ultrasonic = UltrasonicSensor("in2")

# Here's some helper functions to reduce some of the trial and error.
# Jump to the bottom of the file to seem how to use them.

def wait():
    time.sleep(0.1)

def rotate(neg):
    # rotate(1): clockwise 90 degrees.
    # rotate(-1): counterclockwise 90 degrees.
    leftMotor.on_for_seconds(neg * 10, 1.6, block=False)
    rightMotor.on_for_seconds(-neg * 10, 1.6)
    wait()

def forward():
    rightMotor.on_for_seconds(20, 1.9, block=False)
    leftMotor.on_for_seconds(20, 1.9)
    wait()

def doInstruction(command):
    if command == "L": rotate(-1)
    elif command == "R": rotate(1)
    forward()

# Let's copy paste the instructions ...

# Green Wall    |  RLLLLLLL...
# Red Wall      |  LLRLLR...
# Blue Wall     |  RRLLRRLL...
# Green No Wall |  FFF...
# Red No Wall   |  LRLRLR...
# Blue No Wall  |  FRFRFR...

# ... and let the robot know what they are

instructions_green_wall = ["R", "L"]
instructions_red_wall = ["L", "L", "R"]
instructions_blue_wall = ["R", "R", "L", "L"]
instructions_green_empty = ["F"]
instructions_red_empty = ["L", "R"]
instructions_blue_empty = ["F", "R"]

# Let's make some counters
green_wall = 0
red_wall = 0
blue_wall = 0
green_empty = 0
red_empty = 0
blue_empty = 0

password = ""

while True:
    r, g, b = color.rgb
    DistanceToWall = ultrasonic.distance_centimeters

    isWall = DistanceToWall <= 5
    
    if r + g + b >= 300: break
    elif r >= 200:
        password += "R"
        if isWall:
            doInstruction(instructions_red_wall[red_wall])
            if red_wall == 2:
                red_wall = 0
            else:
                red_wall += 1
        else:
            doInstruction(instructions_red_empty[red_empty])
            if red_empty == 1:
                red_empty = 0
            else:
                red_empty += 1
    elif g >= 200:
        password += "G"
        if isWall:
            doInstruction(instructions_green_wall[green_wall])
            if green_wall == 0:
                green_wall += 1
        else:
            doInstruction(instructions_green_empty[green_empty])
    elif b >= 200:
        password += "B"
        if isWall:
            doInstruction(instructions_blue_wall[blue_wall])
            if blue_wall == 3:
                blue_wall = 0
            else:
                blue_wall += 1
        else:
            doInstruction(instructions_blue_empty[blue_empty])
            if blue_empty == 1:
                blue_empty = 0
            else:
                blue_empty += 1
    else:
        break

    print(password)

print(f"Password is {password}")
CommandSystem.send_command(CommandSystem.TYPE_CUSTOM, password)