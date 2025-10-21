class DMXErrorManager:
    """
    Správa chyb v systému DMX – pomocí bitového pole LED_ERR.
    Každý bit odpovídá jedné chybě (např. spojení, čtení, zápis, ...).
    """

    ERROR_BITS = {
        "CONNECTION": 0,  # bit 0
        "READ": 1,        # bit 1
        "WRITE": 2,       # bit 2
        "DEVICE": 3,      # bit 3
    }

    def __init__(self):
        self.LED_ERR = 0

    def set_error(self, name: str):
        """Nastaví příslušný bit chyby."""
        bit = self.ERROR_BITS.get(name)
        if bit is None:
            raise ValueError(f"Neznámý typ chyby: {name}")
        self.LED_ERR |= (1 << bit)

    def clear_error(self, bitmask: int):
        """Smaže chybu (bit na 0)."""
        self.LED_ERR &= ~bitmask
        print(f"[ErrorManager] Smazána chyba: {bin(self.LED_ERR)}")

    def reset_errors(self, check_func):
        """
        Pokusí se resetovat chyby.
        :param check_func: funkce, která vrací True, pokud chyba stále existuje
        """
        for bit in range(32):  # předpokládáme max 32 chyb
            mask = 1 << bit
            if self.LED_ERR & mask:  # pokud je chyba aktivní
                if check_func():
                    print(f"[ErrorManager] Chybu {bit} nelze resetovat, stále aktivní.")
                else:
                    self.clear_error(mask)
                    print(f"[ErrorManager] Chyba {bit} byla úspěšně resetována.")