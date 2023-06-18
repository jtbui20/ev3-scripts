import time
from ev3dev2.motor import LargeMotor

grid = eval(input())

horizontalMotor = LargeMotor("outA")
verticalMotor = LargeMotor("outB")

# Here's some helper functions to reduce some of the trail and error.

def wait():
    time.sleep(0.1)

# Your code goes here
print("Grid is", grid)
new_grid = []
for row in grid:
    row_array = []
    for column in row:
        row_array.append(column)
    new_grid.append(row_array)
    print(row_array)

# Replace the old grid with the cooler grid
grid = new_grid
# We ALWAYS start at 0,0
x = 0
y = 0
time = 0.75
# If 0.75 for 9cm
# How long for 1cm?
tileLength = 9
SecondsPerUnit = tileLength / time

def ChangeGridPos(direction):
    global x, y
    if direction == "R": x += 1
    elif direction == "L": x -= 1
    elif direction == "D": y += 1
    elif direction == "U": y -= 1

while True:
    command = grid[y][x]
    if command == "E":
        break
    ChangeGridPos(command)

DistanceX = x * tileLength
DistanceY = y * tileLength

print(x,y)

RatioX = DistanceX / (DistanceX + DistanceY)
RatioY = DistanceY / (DistanceX + DistanceY)

if max(RatioX, RatioY) == RatioX:
    diff = 1 / RatioX
    RatioX = 1
    RatioY *= diff
else:
    diff = 1 / RatioY
    RatioY = 1
    RatioX *= diff

import math
Time = math.sqrt(((DistanceX * SecondsPerUnit) ** 2) + (DistanceY * SecondsPerUnit) ** 2)

horizontalMotor.on_for_seconds(RatioX * 100, Time, block=False)
verticalMotor.on_for_seconds(RatioY * 100, Time)