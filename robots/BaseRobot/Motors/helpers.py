import math


def ClampSpeed(values, speed=100):
    """Changes the highest motor speed to the speed specified while maintaining the ratio of the other motors"""
    high = max([abs(x) for x in values])
    if high == 0 or speed == 0:
        return values
    ratio = speed / high
    return [min(speed, max(-100, ratio * x)) for x in values]


def AddMatrix(A, B):
    return [A[i] + B[i] for i in range(0, len(A))]


def AngleBetween(current, target):
    """Gets the difference between two directions"""
    angle_dif = ((current - target + 180) % 360) - 180
    return angle_dif


def RadialMove(
    angle,
    speed=100,
    motor_count=4,
    motor_order_offset=1,
):
    """Takes an angle that you want to travel in and sets the current direction to it"""
    values = [0] * motor_count
    # If speed is 0, set values to 0
    if speed != 0:
        theta = math.radians(angle)
        values = [
            math.sin(theta - ((i + motor_order_offset) * math.pi / 2) - math.pi / 4)
            for i in range(0, motor_count)
        ]

        values = ClampSpeed(values, speed)

    return values


def RadialTurn(
    currentAngle,
    targetAngle,
    spread=30,
    speed=10,
    motor_count=4,
    motor_order_offset=1,
):
    """Takes an angle that you want to turn towards and sets motor values to it"""
    differenceAngle = AngleBetween(currentAngle, targetAngle)

    values = [0] * motor_count
    if -spread < differenceAngle < spread:
        return values
    elif differenceAngle < -spread:
        values = [speed, 0, speed, 0]
    elif spread < differenceAngle:
        values = [0, -speed, 0, -speed]
    return values
