# Strategy 1: Move along the axis (no rotation)

x = int(input())
y = int(input())

print(f"Green X={x}")
print(f"Green Y={y}")

# Pick which motors we want to use
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

horizontalMotor = LargeMotor(OUTPUT_A)
verticalMotor = LargeMotor(OUTPUT_B)

# Record some information from the brief.
initialSpawnPoint_x = -50
initialSpawnPoint_y = 35

# Speed is found by testing how long it takes to move from right side to the middle (or top to middle)
# This is probably the longest part of the tasks
timeTakenToMiddle = 1.9

# Use distance / time = speed
speed = 50 / timeTakenToMiddle

# Determine how far we need to move
distanceToRight = x - initialSpawnPoint_x
# We are going in the opposite direction so we need to multiply by -1 (positive -> negative)
distanceToDown = (y - initialSpawnPoint_y) * -1 

# Step 1: Move to the right.
# We can also do non-blocking to move both motors at the same time (change the boolean below)
useBlocking = True
horizontalMotor.on_for_seconds(100, distanceToRight / speed, block=useBlocking)

# Step 2: Move down to the flag at position x, y.
verticalMotor.on_for_seconds(100, distanceToDown / speed)