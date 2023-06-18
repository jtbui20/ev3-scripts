#!/usr/bin/env

from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4

from ev3sim.code_helpers import is_sim

driver_name_compass = "ht-nxt-compass"
driver_name_infrared = "ht-nxt-ir-seek-v2"

default_sensor_configuration = [
  (INPUT_1, UltrasonicSensor, None),
  (INPUT_2, Sensor, driver_name_compass),
  (INPUT_3, Sensor, driver_name_infrared),
  (INPUT_4, UltrasonicSensor, None)
]


class CircularSensorModule:
  def __init__(self, sensor_configuration = default_sensor_configuration):
    self.sensorReference = {}
    for port, sensorType, driver in sensor_configuration:
      if sensorType == Sensor:
        self.sensorReference[port] = sensorType(port, driver_name = driver)
      else:
        self.sensorReference[port] = sensorType(port)

      # Per sensor default configuration
      if sensorType == Sensor:
          if driver is driver_name_infrared:
            self.sensorReference[port].mode = "AC-ALL"
      elif sensorType == UltrasonicSensor:
          self.sensorReference[port].mode = UltrasonicSensor.MODE_US_DIST_CM