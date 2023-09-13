#!/usr/bin/env

from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4

from ev3sim.code_helpers import is_sim

from SensorModule import IRSeeker360

driver_name_compass = "ht-nxt-compass"
driver_name_infrared = "ht-nxt-ir-seek-v2"

default_sensor_configuration = [
  (INPUT_1, UltrasonicSensor),
  (INPUT_2, Sensor, driver_name_compass),
  (INPUT_3, Sensor, driver_name_infrared),
  (INPUT_4, UltrasonicSensor)
]

class SensorModule():
   def __init__(self, sensor_configuration = default_sensor_configuration, debug=False):
      self.sensorReferences = dict[str, any] = {}
      for port, sensorType, driver in sensor_configuration:
        if sensorType == Sensor:
          self.sensorReferences[port] = sensorType(port, driver_name = driver)
          if driver is driver_name_infrared:
            self.sensorReferences[port].mode = "AC-ALL"
        elif sensorType == IRSeeker360:
          self.sensorReferences[port] = IRSeeker360(port)
        else:
          self.sensorReferences[port] = sensorType(port)
          if (sensorType == UltrasonicSensor):
            self.sensorReferences[port].mode = self.sensorReferences[port].MODE_US_DIST_CM