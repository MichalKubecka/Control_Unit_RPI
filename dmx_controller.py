import json
from typing import Optional
from dmx_system import DMXSystem, DMXDevice


class DMXController:
    """
    Controller přijímá JSON příkazy a volá odpovídající metody DMXSystem nebo DMXDevice.
    """
    def __init__(self, system: DMXSystem):
        self.system = system

    def handle_command(self, json_str: str):
        """
        Zpracuje JSON, který může obsahovat jeden příkaz nebo pole příkazů.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            print("[Controller] Chybný JSON:", json_str)
            return

        # Pokud JSON obsahuje více příkazů
        if "commands" in data:
            for cmd in data["commands"]:
                self._execute_single_command(cmd)
        else:
            # Jednoduchý single-command JSON
            self._execute_single_command(data)


    def _execute_single_command(self, cmd: dict):
        action = cmd.get("action")
        if action == "set_value":
            self._set_value(cmd)
        elif action == "set_all":
            self._set_all(cmd)
        elif action == "set_channels":
            self._set_channels(cmd)
        elif action == "add_device":
            self._add_device(cmd)
        elif action == "list_devices":
            self._list_devices(cmd)
        elif action == "reset_errors":
            self.system.error_manager.reset_errors(lambda: True)
        else:
            print(f"[Controller] Neznámá akce: {action}")

    # -------------------- Privátní metody --------------------

    def _find_device(self, name: Optional[str]) -> Optional[DMXDevice]:
        for device in self.system.devices:
            if device.name == name:
                return device
        print(f"[Controller] Zařízení '{name}' nenalezeno.")
        return None

    def _set_value(self, cmd: dict):
        device = self._find_device(cmd.get("device"))
        channel = cmd.get("channel")
        value = cmd.get("value")
        if device is None or channel is None or value is None:
            print("[Controller] Neúplný příkaz pro set_value:", cmd)
            return
        device.set_value(channel, value)

    def _set_all(self, cmd: dict):
        device = self._find_device(cmd.get("device"))
        value = cmd.get("value")
        if device is None or value is None:
            print("[Controller] Neúplný příkaz pro set_all:", cmd)
            return
        device.write([value] * device.channel_count)

    def _set_channels(self, cmd: dict):
        """
        Nastaví více kanálů zařízení podle pole hodnot.
        """
        device = self._find_device(cmd.get("device"))
        values = cmd.get("values")

        if device is None or values is None:
            print("[Controller] Neúplný příkaz pro set_channels:", cmd)
            return

        # Ošetření délky pole hodnot, aby nepřekročila počet kanálů zařízení
        max_len = min(len(values), device.channel_count)
        device.write(values[:max_len])
        print(f"[Controller] Zařízení {device.name} nastaveno hodnotami {values[:max_len]}")

    def _add_device(self, cmd: dict):
        name = cmd.get("device")
        start = cmd.get("start_channel")
        count = cmd.get("channel_count")

        if not all([name, start, count]):
            print("[Controller] Neúplný příkaz pro add_device:", cmd)
            return

        device = self.system.add_device(name=name, start_channel=start, channel_count=count)
        if device is None:
            print(f"[Controller] Nové zařízení {name} nebylo přidáno.")
            return
        print(f"[Controller] Přidáno nové zařízení: {device.name}")
    
    def _list_devices(self, cmd: dict):
        if not self.system.devices:
            print("[Controller] Žádná zařízení nejsou registrována.")
            return

        print("[Controller] Seznam zařízení:")
        for device in self.system.devices:
            print(f" - {device.name}, kanály {device.start_channel}-{device.start_channel + device.channel_count - 1}")