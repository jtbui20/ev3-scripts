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
time = 0.7

def MoveInDirection(direction):
    global x, y
    if direction == "R":
        horizontalMotor.on_for_seconds(100, time)
        x += 1
    elif direction == "L":
        horizontalMotor.on_for_seconds(-100, time)
        x -= 1
    elif direction == "D":
        verticalMotor.on_for_seconds(100, time)
        y += 1
    elif direction == "U":
        verticalMotor.on_for_seconds(-100, time)
        y -= 1

while True:
    command = grid[y][x]
    if command == "E":
        break
    MoveInDirection(command)