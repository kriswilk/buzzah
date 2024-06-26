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
# Vibration amplitude range, in %
AMPLITUDE_MIN = 100
AMPLITUDE_MAX = 100
# Duration of each vibration and subsequent pause, each in seconds
TIME_ON = 0.100
TIME_OFF = 0.067
# Duration of the relaxation period between sets of vibrations, in seconds
TIME_RELAX = 4 * (TIME_ON + TIME_OFF)
# Jitter, in %
JITTER = 23.5
# Mirror left / right hand vibration patterns
MIRROR = False
# Duration of the therapy session, in minutes
TIME_SESSION = 120

### DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING ###

# Precomputed data
TIME_JITTER = (TIME_ON + TIME_OFF) * (JITTER / 100) / 2
TIME_END = time.time() + 60 * TIME_SESSION
PATTERNS_LEFT = list(adafruit_itertools.permutations(range(0, 4)))
PATTERNS_RIGHT = list(adafruit_itertools.permutations(range(4, 8)))

def random_sequence():
  pattern_left = random.choice(PATTERNS_LEFT)
  if MIRROR:
    pattern_right = [x+4 for x in pattern_left]
  else:
    pattern_right = random.choice(PATTERNS_RIGHT)
  return zip(pattern_left, pattern_right)

def fingers_on(fingers):
  for finger in fingers:
    if drivers[finger]:
      drivers[finger].realtime_value = random.randint(AMPLITUDE_MIN, AMPLITUDE_MAX)

def fingers_off(fingers):
  for finger in fingers:
    if drivers[finger]:
      drivers[finger].realtime_value = 0

def buzz_sequence(sequence):
  for fingers in sequence:
    fingers_on(fingers)
    time.sleep(TIME_ON)
    fingers_off(fingers)
    time.sleep(TIME_OFF + random.uniform(-TIME_JITTER, TIME_JITTER))

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
    if ACTUATOR_TYPE == "LRA":
      driver.use_LRM()
    else:
      driver.use_ERM()
    
    # set open-loop mode (both ERM & LRA)
    control3 = driver._read_u8(0x1D)
    driver._write_u8(0x1D, control3 | 0x21)

    # set peak voltage
    driver._write_u8(0x17, int(ACTUATOR_VOLTAGE / 0.02122))

    # set driving frequency
    driver._write_u8(0x20, int(1 / (ACTUATOR_FREQUENCY * 0.00009849)))

    # set initial output amplitude and activate RTP mode
    driver.realtime_value = 0
    driver.mode = adafruit_drv2605.MODE_REALTIME

while time.time() < TIME_END:
  buzz_sequence(random_sequence())
  buzz_sequence(random_sequence())
  buzz_sequence(random_sequence())
  time.sleep(TIME_RELAX)
  time.sleep(TIME_RELAX)
