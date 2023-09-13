from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import I2cSensor, Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4

from Sensors import IRSeeker360

class SensorModuleManual():
  def __init__(self):
    self.sensorReferences = {
      INPUT_1: UltrasonicSensor(INPUT_1),
      INPUT_2: Sensor(INPUT_2, driver_name="ht-nxt-compass"),
      INPUT_3: IRSeeker360(INPUT_3),
      INPUT_4: UltrasonicSensor(INPUT_4)
    }

  def __sensorSetup__(self):
    self.sensorReferences[INPUT_1].mode = UltrasonicSensor.MODE_US_DIST_CM
    self.CompassCalibrate();
    self.sensorReferences[INPUT_4].mode = UltrasonicSensor.MODE_US_DIST_CM

  def CompassCalibrate(self):
    self.sensorReferences[INPUT_2].command = "BEGIN-CAL"
    self.sensorReferences[INPUT_2].command = "END-CAL"

  def GetSensorValue(self, port, **kwargs):
    '''Use this so that we can log values if we want to'''
    if port in self.sensorReferences:
      if port == INPUT_1:
        return self.sensorReferences[port].value(0)
      elif port == INPUT_2:
        return self.sensorReferences[port].value(0)
      elif port == INPUT_3:
        return self.sensorReferences[port].value()
      elif port == INPUT_4:
        return self.sensorReferences[port].value(0)
    else:
      raise Exception("Sensor port not found")