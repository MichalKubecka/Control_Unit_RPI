from pymodbus.client import ModbusTcpClient
import loguru as log
import rich
import gpiozero as gpio
from adafruit_pca9685 import PCA9685

from dmx_device import DMXDevice
from dmx_error import DMXErrorManager

status_meaning = {
    0: "data jsou platná",
    1: "probíhá inicializace",
    4: "chyba",
}
class DMXSystem:
    """ Singleton class """
    _instance = None

    def __new__(cls, ip, port, timeout=2):
        if cls._instance is None:                   # 1) Pokud ještě instance neexistuje
            cls._instance = super().__new__(cls)    # 2) vytvoř novou instanci
            cls._instance._initialized = False      # 3) příznak, že ještě není inicializována
        return cls._instance                        # 4) vrátí buď novou, nebo už existující instanci   

    def __init__(self, ip, port, timeout=2):
        if self._initialized: return
        self.ip = ip
        self.port = port
        self.client = ModbusTcpClient(host=ip, port=port, timeout=timeout)
        self.error_manager = DMXErrorManager()
        self.devices = []
        self.infile = 'input.txt'
        self.NEW_VALUE = None
        self.OLD_VALUE = None
        self.controller = None
        self._initialized = True

    # --- Sprava spojeni --------------

    def connect(self):
        if not self.client.connect():
            raise RuntimeError("Nepodařilo se navázat Modbus TCP spojení.")
            self.error_manager.set_error("CONNECTION")
            return -1
        return 0

    def disconnect(self):
        self.client.close()

    # --- Metody controlleru ----------
    def set_controller(self, controller):
        self.controller = controller
        print(f"[DMXSystem] Controller nastaven: {controller}")

    # --- DMX management methods ------

    def add_device(self, name: str, start_channel: int, channel_count: int) -> DMXDevice:
        """
        Vytvoří nové zařízení a přidá ho do seznamu systému.
        Vrací objekt DMXDevice.
        """
        # Kontrola duplicit
        if any(d.name == name for d in self.devices):
            print(f"[DMXSystem] Zařízení s názvem '{name}' již existuje.")
            return None
        device = DMXDevice(system=self, name=name, start_channel=start_channel, channel_count=channel_count)
        self.devices.append(device)
        print(f"[DMXSystem] Přidáno zařízení: {device}")
        return device

    def _read_variable_from_file(self):
        try:
            with open(self.infile, "r") as f:
                value = f.read().strip()
                self.NEW_VALUE = value
                return int(value)
        except Exception as e:
            print(f"Chyba při čtení souboru: {e}")
            return None

    def read_channels(self, start: int, count: int) -> list[int]:
        """
        Načte hodnoty z registrů Modbus od start adresy.
        :param start: startovní registr (DMX kanál)
        :param count: počet registrů ke čtení
        :return: seznam hodnot registrů
        """
        rr = self.client.read_holding_registers(address=start, count=count)
        if rr.isError():
            raise RuntimeError(f"Chyba při čtení registrů {start}-{start+count-1}: {rr}")
        return rr.registers

    def write_channel(self, address: int, value: int):
        """
        Zapíše jednu hodnotu do registru Modbus.
        """
        wr = self.client.write_register(address=address, value=value)
        if wr.isError():
            raise RuntimeError(f"Chyba při zápisu do registru {address}: {wr}")
        print(f"[DMXSystem] Zapsáno: registr {address} = {value}")

    def write_channels(self, start: int, values: list[int]):
        """
        Zapíše více hodnot do registrů postupně od start adresy.
        """
        for i, val in enumerate(values):
            self.write_channel(start + i, val)
