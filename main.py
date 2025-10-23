from misc import *
from dmx_system import DMXSystem
from dmx_controller import DMXController
from dmx_error import DMXErrorManager
import time


# ----- Setup -------------------------
dmx = DMXSystem(ip="192.168.8.60", port=502)
dmx.connect()

# Inicializace správce chyb
dmx.error_manager = DMXErrorManager()

# Inicializace controlleru
controller = DMXController(dmx)
dmx.set_controller(controller)

# Inicializace zařízení
front_light = dmx.add_device("FrontLight", start_channel=101, channel_count=4)
motor = dmx.add_device("Motor", start_channel=105, channel_count=2) # TODO not used

# Paměť poslední hodnoty JSON
OLD_JSON = None


# ----- Loop --------------------------
try:
    while True:
        time.sleep(0.25)  # perioda kontroly

        # Čtení JSON příkazu ze souboru
        NEW_JSON = read_variable_from_file("input.txt")
        if NEW_JSON is None:
            continue

        # Pokud se JSON změnil
        if NEW_JSON != OLD_JSON:
            print(f"[MAIN] Nový příkaz: {NEW_JSON}")

            # Předání příkazu controlleru přímo
            controller.handle_command(NEW_JSON)

            OLD_JSON = NEW_JSON

except KeyboardInterrupt:
    print("[MAIN] Ukončuji smyčku...")
finally:
    dmx.disconnect()
    print("[MAIN] Spojení s DMX uzavřeno.")
