import can
import struct
import time

# Node ID van jouw ODrive
NODE_ID = 1
ENCODER_POS_RTR_ID = 0x009 + NODE_ID

print("Start CAN-bus (can0)...")
bus = can.interface.Bus(channel='can0', bustype='socketcan')

while True:
    # Vraag positie op met Remote Frame (RTR)
    rtr_msg = can.Message(arbitration_id=ENCODER_POS_RTR_ID,
                          is_extended_id=False,
                          is_remote_frame=True,
                          dlc=4)  # Verwacht 4 bytes als antwoord

    try:
        bus.send(rtr_msg)
        print(f"RTR verzonden naar ID {hex(ENCODER_POS_RTR_ID)}")
    except can.CanError:
        print("Fout bij verzenden van CAN-verzoek")

    # Wacht op antwoord met dezelfde ID
    timeout = 1.0  # seconde
    response = bus.recv(timeout)

    if response and response.arbitration_id == ENCODER_POS_RTR_ID:
        if len(response.data) == 4:
            # Float uitpakken (4 bytes, little endian)
            pos, = struct.unpack('<f', response.data)
            print(f"Encoder Positie: {pos}")
        else:
            print(f"Ongeldige data: {response.data}")
    else:
        print("Geen geldig antwoord ontvangen")

    time.sleep(1)  # Wacht even voor volgende verzoek

