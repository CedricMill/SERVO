import can
import time
import math
import struct

# Stel hier je ODrive CAN node-ID in (standaard 0x01)
NODE_ID = 0x01

# CAN commando-ID's (volgens ODrive CAN protocol)
SET_INPUT_POS_ID = 0x00C  # 0x00C = Set Input Position command

# Instellen van frequentie en amplitude van de sinus
FREQUENCY_HZ = 0.5      # halve cyclus per seconde
AMPLITUDE_TURNS = 1.0   # sinus schommelt tussen -1 en 1 om 0
OFFSET_TURNS = 0        # als je niet rond 0 wil schommelen

# Ophaalperiode (in seconden)
UPDATE_INTERVAL = 0.02  # 50 Hz

# Totale tijdsduur om te bewegen (in seconden)
RUN_DURATION = 20

def float_to_bytes(value):
    """Zet float32 om naar 4 bytes in little-endian formaat"""
    return struct.pack("<f", value)

def send_input_position(bus, position_turns):
    """
    Stuurt een 'Set Input Position' commando naar de ODrive.
    """
    data = float_to_bytes(position_turns) + bytes([0, 0, 0, 0])  # 4 bytes voor velden vel=0, accel=0
    msg = can.Message(
        arbitration_id=(NODE_ID << 5) | SET_INPUT_POS_ID,
        data=data,
        is_extended_id=False
    )
    try:
        bus.send(msg)
    except can.CanError as e:
        print(f"CAN-fout: {e}")

def main():
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    print("Start sinusbeweging...")

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > RUN_DURATION:
            break

        # Bereken sinuspositie
        angle = 2 * math.pi * FREQUENCY_HZ * elapsed
        position = OFFSET_TURNS + AMPLITUDE_TURNS * math.sin(angle)

        # Verstuur de positie
        send_input_position(bus, position)

        # Even wachten voor volgende update
        time.sleep(UPDATE_INTERVAL)

    print("Sinusbeweging afgerond.")

if __name__ == "__main__":
    main()
