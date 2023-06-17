# Strategy 2: Move along the axis (with rotation)

x = int(input())
y = int(input())

print(f"Green X={x}")
print(f"Green Y={y}")

# Pick which motors we want to use
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

LeftMotor = LargeMotor(OUTPUT_A)
RightMotor = LargeMotor(OUTPUT_B)

# Record some information from the brief.
initialSpawnPoint_x = -50
initialSpawnPoint_y = 35

# Speed is found by testing how long it takes to move from right side to the middle (or top to middle)
# This is probably the longest part of the tasks
timeTakenToMiddle = 1.9

# Use distance / time = speed
# Speed is double because we're applying more force
speed = 100 / timeTakenToMiddle

# We also need to add turning speed in 
turnDuration = 90 / 510

# Determine how far we need to move
distanceToRight = x - initialSpawnPoint_x
# We are going in the opposite direction so we need to multiply by -1 (positive -> negative)
distanceToDown = (y - initialSpawnPoint_y) * -1 

LeftMotor.on_for_seconds(100, distanceToRight / speed, block=False)
RightMotor.on_for_seconds(100, distanceToRight / speed)

LeftMotor.on_for_seconds(100, turnDuration, brake=True, block=False)
RightMotor.on_for_seconds(-100, turnDuration, brake=True)

LeftMotor.on_for_seconds(100, distanceToDown / speed, block=False)
RightMotor.on_for_seconds(100, distanceToDown / speed)