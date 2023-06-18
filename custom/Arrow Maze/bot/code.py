import time
from ev3dev2.motor import LargeMotor

grid = eval(input())

topMotor = LargeMotor("outA")
botMotor = LargeMotor("outB")

# Here's some helper functions to reduce some of the trail and error.

def wait():
    time.sleep(0.1)

def rotate(neg):
    # rotate(1): clockwise 90 degrees.
    # rotate(-1): counterclockwise 90 degrees.
    topMotor.on_for_seconds(neg * 10, 1.6, block=False)
    botMotor.on_for_seconds(-neg * 10, 1.6)
    wait()

def forward():
    botMotor.on_for_seconds(20, 1.9, block=False)
    topMotor.on_for_seconds(20, 1.9)
    wait()


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

old_command = "R"

while True:
    command = grid[y][x]
    print(grid[y][x])
    if command == "R":
        if old_command == "U":
            rotate(1)
        elif old_command == "D":
            rotate(-1)
        forward()
        x += 1
    elif command == "D":
        if old_command == "R":
            rotate(1)
        elif old_command == "L":
            rotate(-1)
        forward()
        y += 1
    elif command == "L":
        if old_command == "D":
            rotate(1)
        elif old_command == "U":
            rotate(-1)
        forward()
        x -= 1
    elif command == "U":
        if old_command == "L":
            rotate(1)
        elif old_command == "R":
            rotate(-1)
        forward()
        y -= 1
    else:
        break

    old_command = command