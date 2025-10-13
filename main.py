from dmx_system import DMXSystem
from functions import read_variable_from_file
import time


# ----- Setup -------------------------
dmx = DMXSystem(ip="192.168.8.60", port=502, unit=1)
dmx.connect()
front_light = dmx.add_device("FrontLight", start_channel=101, channel_count=4)
motor = dmx.add_device("Motor", start_channel=105, channel_count=2) # TODO not used


# ----- Loop --------------------------
OLD_VALUE = None
try:
    while True:
        time.sleep(0.25)  # perioda kontroly
        NEW_VALUE = read_variable_from_file("input.txt")
        if NEW_VALUE is None:
            continue

        if NEW_VALUE != OLD_VALUE:
            print(f"Změna detekována: {OLD_VALUE} -> {NEW_VALUE}")

            # zápis do všech kanálů FrontLight
            front_light.write([NEW_VALUE] * front_light.channel_count)
            # případně zápis i do motoru
            OLD_VALUE = NEW_VALUE

except KeyboardInterrupt:
    print("Ukončuji smyčku...")
finally:
    dmx.disconnect()
