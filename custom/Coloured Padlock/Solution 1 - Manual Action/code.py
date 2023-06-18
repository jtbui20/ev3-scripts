import time
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor

horizontalMotor = LargeMotor("outA")
verticalMotor = LargeMotor("outB")
color = ColorSensor("in1")

# Write some code here!
UnitsPerSecond = 26.316
SecondsPerUnit = 1.0 / UnitsPerSecond

# Go down 70cm
verticalMotor.on_for_seconds(100, 70 * SecondsPerUnit)

# Go right 26.7cm
horizontalMotor.on_for_seconds(100, 26.7 * SecondsPerUnit)

# Find out which colour we're working with
# If you're lazy, you can use color.color()
time.sleep(0.5)
r, g, b = color.rgb
print(r, g, b)

if r >= 200:
    # If it's red, we go 70cm up
    verticalMotor.on_for_seconds(-100, 70 * SecondsPerUnit)
    # Then we slide in and out
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 70 * SecondsPerUnit)
elif g >= 200:
    # If it's red, we go 47.5 up
    verticalMotor.on_for_seconds(-100, 47.5 * SecondsPerUnit)
    # Then we slide in and out
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 47.6 * SecondsPerUnit)
elif b >= 200:
    # If it's red, we go 24.17 up
    verticalMotor.on_for_seconds(-100, 24.17 * SecondsPerUnit)
    # Then we slide in and out
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 24.17 * SecondsPerUnit)

# Haha copy paste go brrrrrr

horizontalMotor.on_for_seconds(100, 32.5 * SecondsPerUnit)

time.sleep(0.5)
r, g, b = color.rgb
print(r, g, b)

if r >= 200:
    verticalMotor.on_for_seconds(-100, 70 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 70 * SecondsPerUnit)
elif g >= 200:
    verticalMotor.on_for_seconds(-100, 47.5 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 47.6 * SecondsPerUnit)
elif b >= 200:
    verticalMotor.on_for_seconds(-100, 24.17 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 24.17 * SecondsPerUnit)

horizontalMotor.on_for_seconds(100, 32.5 * SecondsPerUnit)

time.sleep(0.5)
r, g, b = color.rgb
print(r, g, b)

if r >= 200:
    verticalMotor.on_for_seconds(-100, 70 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 70 * SecondsPerUnit)
elif g >= 200:
    verticalMotor.on_for_seconds(-100, 47.5 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 47.6 * SecondsPerUnit)
elif b >= 200:
    verticalMotor.on_for_seconds(-100, 24.17 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(100, 13.3 * SecondsPerUnit)
    horizontalMotor.on_for_seconds(-100, 13.3 * SecondsPerUnit)
    verticalMotor.on_for_seconds(100, 24.17 * SecondsPerUnit)

horizontalMotor.on_for_seconds(100, 10 * SecondsPerUnit)