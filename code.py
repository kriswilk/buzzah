import adafruit_drv2605
import adafruit_itertools
import adafruit_tca9548a
import board
import random
import time

AMPLITUDE = 127
JITTER = 23.5

T_ON = 0.100
T_OFF = 0.067
T_STEP = T_ON + T_OFF
T_CR = 4 * T_STEP
T_JITTER = T_STEP * (JITTER / 100) / 2

PATTERNS_LEFT = list(adafruit_itertools.permutations(range(0, 4)))
PATTERNS_RIGHT = list(adafruit_itertools.permutations(range(4, 8)))

def random_sequence():
  return zip(random.choice(PATTERNS_LEFT), random.choice(PATTERNS_RIGHT))

def fingers_on(fingers):
  for finger in fingers:
    drivers[finger].mode = adafruit_drv2605.MODE_REALTIME

def fingers_off(fingers):
  for finger in fingers:
    drivers[finger].mode = adafruit_drv2605.MODE_INTTRIG

def buzz_sequence(sequence):
  for fingers in sequence:
    fingers_on(fingers)
    time.sleep(T_ON)
    fingers_off(fingers)
    time.sleep(T_OFF + random.uniform(-T_JITTER, T_JITTER))

i2c = board.STEMMA_I2C()
mux = adafruit_tca9548a.TCA9548A(i2c)
drivers = [adafruit_drv2605.DRV2605(port) for port in mux]

for d in drivers:
  d.use_LRM()
  d.realtime_value = AMPLITUDE

while True:
  buzz_sequence(random_sequence())
  buzz_sequence(random_sequence())
  buzz_sequence(random_sequence())
  time.sleep(T_CR)
  time.sleep(T_CR)
