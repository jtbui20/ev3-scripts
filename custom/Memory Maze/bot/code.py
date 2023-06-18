import time
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3sim.code_helpers import CommandSystem

leftMotor = LargeMotor("outA")
rightMotor = LargeMotor("outB")
colourSensor = ColorSensor("in1")
ultrasonic = UltrasonicSensor("in2")

# Declare our variables
instructions = {
    "red": {
        "wall": ["L", "L", "R"],
        "empty": ["L", "R"]
    },
    "green": {
        "wall": ["R", "L"],
        "empty": ["F"]
    },
    "blue": {
        "wall": ["R", "R", "L", "L"],
        "empty": ["F", "R"]
    }
}

counters = {
    "red": {
        "wall": 0,
        "empty": 0
    },
    "green": {
        "wall": 0,
        "empty": 0
    },
    "blue": {
        "wall": 0,
        "empty": 0
    }
}

# Green Wall    |  RLLLLLLL...
# Red Wall      |  LLRLLR...
# Blue Wall     |  RRLLRRLL...
# Green No Wall |  FFF...
# Red No Wall   |  LRLRLR...
# Blue No Wall  |  FRFRFR...

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
    
def processInstructions(colour, isWall):
    wallString = "wall" if isWall else "empty"
    instruction = instructions[colour][wallString]
    counter = counters[colour][wallString]

    command = instruction[counter]
    if command == "L": rotate(-1)
    elif command == "R": rotate(1)
    forward()

    counter += 1
    if (counter >= len(instruction)): 
        if (colour, wallString) != ("green", "wall"): counter = 0
        else: counter -= 1
    counters[colour][wallString] = counter

password = ""

while True:
    colorFound = None
    r,g,b = colourSensor.rgb
    if r + g + b >= 300: break
    elif r >= 200: 
        colorFound = "red"
        password += "R"
    elif g >= 200: 
        colorFound = "green"
        password += "G"
    elif b >= 200: 
        colorFound = "blue"
        password += "B"
    else:
        break

    isWall = ultrasonic.distance_centimeters <= 5

    if colorFound in ["red", "green", "blue"]: processInstructions(colorFound, isWall)

print(f"Password is {password}")
CommandSystem.send_command(CommandSystem.TYPE_CUSTOM, password)