# Plaats deze code in Thonny op je Raspberry Pi

import can
import struct
import time

# 1) Open de CAN-bus (SocketCAN)
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

# 2) Zet hier het node ID van je ODrive (default is 0)
NODE_ID = 0

# Helper: bouw de CANSimple-arbitrage-ID
def cs_id(cmd_id: int) -> int:
    return (NODE_ID << 5) | cmd_id

# 3) Functie om de as in een bepaalde state te zetten
#    CMD_ID 0x07 = Set_Axis_State
#    state: 1=IDLE, 3=CLOSED_LOOP_CONTROL, etc.
def set_axis_state(state: int):
    arb_id = cs_id(0x07)
    # Axis_Requested_State is een 32-bit little-endian veld; padding = 0
    data = struct.pack('<I', state)
    msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id=False)
    bus.send(msg)

# 4) Functie om snelheidscommando te sturen
#    CMD_ID 0x0D = Set_Input_Vel
#    vel en torque_ff zijn IEEE754-floats (4 bytes elk)
def set_input_velocity(vel: float, torque_ff: float = 0.0):
    arb_id = cs_id(0x0D)
    data = struct.pack('<ff', vel, torque_ff)
    msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id=False)
    bus.send(msg)

# 5) Voorbeeld: zet de as in closed-loop control en stuur een velocity
if __name__ == "__main__":
    # Ga naar CLOSED_LOOP_CONTROL (state = 3)
    print("Switching axis to CLOSED_LOOP_CONTROL...")
    set_axis_state(3)
    time.sleep(0.1)  # korte pauze om de state over CAN te laten gaan

    # Stuur een velocity van 1000 counts/s met 0 torque feed-forward
    print("Sending velocity command...")
    set_input_velocity(1000.0, 0.0)

    # Houd het commando even vast (alternatief: in een loop sturen)
    time.sleep(5.0)

    # Stop (ga terug naar IDLE)
    print("Stopping axis...")
    set_axis_state(1)
    ```

**Toelichting**  
- We gebruiken `socketcan_native` zodat Python-CAN direct op SocketCAN draait. :contentReference[oaicite:0]{index=0}  
- ODrive’s CANSimple-protocol verdeelt de 11-bit ID in een `node_id` (bits 10–5) en `cmd_id` (bits 4–0). :contentReference[oaicite:1]{index=1}  
- `Set_Axis_State` (cmd 0x07) schakelt de as in/uit. `CLOSED_LOOP_CONTROL` is state 3, `IDLE` is state 1.  
- `Set_Input_Vel` (cmd 0x0D) stuurt een snelheid en optioneel torque feed-forward, beide als 32-bit floats.  

Je kunt dit uitbreiden met functies voor posities (`Set_Input_Pos`, cmd 0x0C) of torque (`Set_Input_Torque`, cmd 0x0E`) door dezelfde aanpak te volgen, maar met andere `cmd_id` en `struct.pack`-formats.
::contentReference[oaicite:2]{index=2}
