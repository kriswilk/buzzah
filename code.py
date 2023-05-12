import adafruit_drv2605
import adafruit_itertools
import adafruit_tca9548a
import board
import math
import random
import time

"""
ACTUATOR SPECIFICATIONS: These MUST be set to match the specifications of the
actuator that you are using.
"""
# Type of actuator: "LRA" or "ERM"
ACTUATOR_TYPE = "LRA"
# Maximum drive voltage, in V
ACTUATOR_VOLTAGE = 1.8 * math.sqrt(2)
# Driving frequency, in Hz
ACTUATOR_FREQUENCY = 235

"""
COORDINATED RESET PARAMETERS: These are based on the published research. You are
free to change them to alter the behaviour of the device.
"""
# Vibration amplitude, in % (reduce if the vibration is too intense)
AMPLITUDE = 100
# Duration of each vibration and subsequent pause, each in s
TIME_ON = 0.100
TIME_OFF = 0.067
# Duration of the relaxation period between sets of vibrations, in s
TIME_RELAX = 4 * (TIME_ON + TIME_OFF)
# Jitter, in %
JITTER = 23.5

### DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING ###

# Precomputed data
T_JITTER = (TIME_ON + TIME_OFF) * (JITTER / 100) / 2
PATTERNS_LEFT = list(adafruit_itertools.permutations(range(0, 4)))
PATTERNS_RIGHT = list(adafruit_itertools.permutations(range(4, 8)))

def random_sequence():
  return zip(random.choice(PATTERNS_LEFT), random.choice(PATTERNS_RIGHT))

def fingers_on(fingers):
  for finger in fingers:
    if drivers[finger]:
      drivers[finger].realtime_value = AMPLITUDE

def fingers_off(fingers):
  for finger in fingers:
    if drivers[finger]:
      drivers[finger].realtime_value = 0

def buzz_sequence(sequence):
  for fingers in sequence:
    fingers_on(fingers)
    time.sleep(TIME_ON)
    fingers_off(fingers)
    time.sleep(TIME_OFF + random.uniform(-T_JITTER, T_JITTER))

i2c = board.STEMMA_I2C()
mux = adafruit_tca9548a.TCA9548A(i2c)

drivers = []
for port in mux:
  try:
    drivers.append(adafruit_drv2605.DRV2605(port))
  except ValueError:
    drivers.append(False)

for driver in drivers:
  if driver:
    # set actuator type
    feedback = driver._read_u8(0x1A)
    if ACTUATOR_TYPE == "LRA":
      feedback |= 0x80
    else:
      feedback &= 0x7F
    driver._write_u8(0x1A, feedback)

    # run both ERM and LRA in open-loop mode
    control3 = driver._read_u8(0x1D)
    driver._write_u8(0x1D, control3 | 0x21)

    # set OL_CLAMP voltage
    driver._write_u8(0x17, int(ACTUATOR_VOLTAGE / 0.02122))

    # set driving frequency
    driver._write_u8(0x20, int(1 / (ACTUATOR_FREQUENCY * 0.00009849)))

    # set initial output amplitude and activate RTP mode
    driver._write_u8(0x02, 0x00)
    driver._write_u8(0x01, 0x05)    

while True:
  buzz_sequence(random_sequence())
  buzz_sequence(random_sequence())
  buzz_sequence(random_sequence())
  time.sleep(TIME_RELAX)
  time.sleep(TIME_RELAX)
