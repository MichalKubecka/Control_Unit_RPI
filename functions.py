def read_variable_from_file(filename):
    try:
        with open(filename, "r") as f:
            return int(f.read().strip())
    except Exception as e:
        print(f"Chyba při čtení souboru: {e}")
        return None