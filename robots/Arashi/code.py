import time
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor import Sensor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor

# IR sensor
irs = Sensor("in1", driver_name="ht-nxt-ir-seek-v2")
irs.mode = "AC-ALL"
# Color sensor to color
cls = ColorSensor("in2")
cls.mode = cls.MODE_RGB_RAW
c_Green = (86, 147, 53)
c_White = (200, 200, 200)
c_Cyan = (42, 162, 179)
c_Black = (0, 0, 0)
# Ultrasonic sensor to cm
us = UltrasonicSensor("in3")
us.mode = us.MODE_US_DIST_CM
# Compass sensor to default
cps = Sensor("in4", driver_name="ht-nxt-compass")
cps.command = 'BEGIN-CAL'
cps.command = 'END-CAL'

m_bl = LargeMotor("outA")
m_fl = LargeMotor("outB")
m_fr = LargeMotor("outC")
m_br = LargeMotor("outD")

def MoveStrafe(dir):
    # ! Order of motor activation matters
    if dir == "forwards":
        m_fl.on(100)
        m_fr.on(100)
        m_br.on(100)
        m_bl.on(100)
    elif dir == "left":
        m_fl.on(-100)
        m_fr.on(100)
        m_br.on(-100)
        m_bl.on(100)
    elif dir == "back":
        m_bl.on(-100)
        m_br.on(-100)
        m_fr.on(-100)
        m_fl.on(-100)
    elif dir == "right":
        m_fl.on(100)
        m_fr.on(-100)
        m_br.on(100)
        m_bl.on(-100)
    elif dir == "stop":
        m_fl.off()
        m_fr.off()
        m_br.off()
        m_bl.off()

def Rotate(dir, pow):
    if dir == "anti":
        m_fr.off()
        m_fl.on(-pow)
        m_br.on(pow)
        m_bl.off()
    elif dir == "clock":
        m_fl.off()
        m_fr.on(-pow)
        m_bl.on(pow)
        m_br.off()

prev = 0
def MoveToBall(val):
    global prev
    if val is prev and not 0: return
    elif val in [1,2,3]: MoveStrafe("left")
    elif val in [4,5,6]: MoveStrafe("forwards")
    elif val in [7,8,9]: MoveStrafe("right")
    else: MoveStrafe("back")
    prev = val

while True:
    irv = irs.value(0)
    ang = cps.value(0)
    col = cls.rgb
    usv = us.distance_centimeters

    if sum(col) >= sum(c_White):
        if usv > 75: MoveStrafe("left")
        else: MoveStrafe("right")
    else:
        if ang > 180: ang -= 360
        angp = 100 * ang / 180
        if ang in range(-30, 30): MoveToBall(irv)
        else: Rotate("clock", angp)
    time.sleep(0.001)