from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor

horizontalMotor = LargeMotor("outA")
verticalMotor = LargeMotor("outB")
color = ColorSensor("in1")

# Write some code here!
UnitsPerSecond = 26.316
SecondsPerUnit = 1.0 / UnitsPerSecond
NumberOfTimes = 3

# A function, check out Python 6 - Functions and common patterns
def doLock(): 
    lock = color.color
    
    if lock == 5:
        # If it's red, we go 70cm up
        verticalMotor.on_for_seconds(-100, 70 * SecondsPerUnit)
        horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
        horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
        verticalMotor.on_for_seconds(100, 70 * SecondsPerUnit)
    elif lock == 3:
        # If it's red, we go 47.5cm up
        verticalMotor.on_for_seconds(-100, 47.5 * SecondsPerUnit)
        horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
        horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
        verticalMotor.on_for_seconds(100, 47.6 * SecondsPerUnit)
    elif lock == 1:
        # If it's red, we go 24.17 up
        verticalMotor.on_for_seconds(-100, 24.17 * SecondsPerUnit)
        horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
        horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
        verticalMotor.on_for_seconds(100, 24.17 * SecondsPerUnit)

# Go down 70cm
verticalMotor.on_for_seconds(100, 70 * SecondsPerUnit)

# Go right 26.7cm
horizontalMotor.on_for_seconds(100, 26.7 * SecondsPerUnit)
c = 0
while c < NumberOfTimes:
    doLock()
    horizontalMotor.on_for_seconds(100, 32.5 * SecondsPerUnit)
    c += 1