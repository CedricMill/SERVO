import odrive
from odrive.enums import *
import time

print("Zoeken naar ODrive...")

# Zoek automatisch naar een verbonden ODrive via USB
odrv = odrive.find_any()

print("Verbonden met ODrive!")
print("Firmware versie:", odrv.fw_version_major, odrv.fw_version_minor, odrv.fw_version_revision)

# Simpele test: lees de bus voltage
print("Bus Voltage:", odrv.vbus_voltage, "V")

# Simpele test: print de huidige encoderpositie van axis0
print("Encoder Positie (axis0):", odrv.axis0.encoder.pos_estimate)

# Eventueel: LED laten knipperen als bevestiging (als ondersteund)
# odrv.axis0.requested_state = AXIS_STATE_IDLE
# time.sleep(1)
# odrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
