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

PATTERNS = list(adafruit_itertools.permutations(range(4)))

def finger_on(finger):
  drivers[finger].mode = adafruit_drv2605.MODE_REALTIME

def finger_off(finger):
  drivers[finger].mode = adafruit_drv2605.MODE_INTTRIG

def buzz_sequence(fingers):
  for finger in fingers:
    finger_on(finger)
    finger_on(finger + 4)
    time.sleep(T_ON)
    finger_off(finger)
    finger_off(finger + 4)
    time.sleep(T_OFF + random.uniform(-T_JITTER, T_JITTER))

i2c = board.STEMMA_I2C()
mux = adafruit_tca9548a.TCA9548A(i2c)
drivers = [adafruit_drv2605.DRV2605(port) for port in mux]

for d in drivers:
  d.use_LRM()
  d.realtime_value = AMPLITUDE

while True:
  buzz_sequence(random.choice(PATTERNS))
  buzz_sequence(random.choice(PATTERNS))
  buzz_sequence(random.choice(PATTERNS))
  time.sleep(T_CR)
  time.sleep(T_CR)
