status_meaning = {
    0: "data jsou platná",
    1: "probíhá inicializace",
    4: "chyba",
}

LED_ERR = 0

def read_variable_from_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Chyba při čtení souboru: {e}")
        return None