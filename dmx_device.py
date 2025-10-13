class DMXDevice:
    def __init__(self, system, name, start_channel, channel_count):
        self.system = system
        self.name = name
        self.start_channel = start_channel
        self.channel_count = channel_count
        self.values = [0] * channel_count


    def read(self):
        self.values = self.system.read_channels(self.start_channel, self.channel_count)


    def write(self, values: list[int]):
        """
        Zapíše všechny hodnoty zařízení do systému.
        """
        if len(values) != self.channel_count:
            raise ValueError("Počet hodnot neodpovídá počtu kanálů zařízení.")
        self.system.write_channels(self.start_channel, values)
        self.values = values
        print(f"[{self.name}] Zápis: {self.values}")


    def set_value(self, index: int, value: int):
        """
        Zapíše hodnotu do jednoho kanálu zařízení.
        """
        if not (0 <= index < self.channel_count):
            raise IndexError("Neplatný index kanálu.")
        self.system.write_channel(self.start_channel + index, value)
        self.values[index] = value
        print(f"[{self.name}] Kanál {index+1} = {value}")