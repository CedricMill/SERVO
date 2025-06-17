import can
import time

# Gebruik de socketcan driver en can0 interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Een testbericht op het CAN-netwerk sturen
msg = can.Message(arbitration_id=0x123, data=[0x11, 0x22, 0x33], is_extended_id=False)

try:
    print("Versturen test CAN-bericht...")
    bus.send(msg)
    print("Bericht verzonden.")

    print("Wachten op een antwoord of echo (timeout 5s)...")
    response = bus.recv(timeout=5.0)
    if response:
        print(f"Ontvangen: ID={hex(response.arbitration_id)} DATA={list(response.data)}")
    else:
        print("Geen antwoord ontvangen.")
except can.CanError as e:
    print(f"Fout bij verzenden: {e}")
