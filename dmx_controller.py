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
        Zpracuje příkaz ve formátu JSON.

        Příklad příkazu:
        {"action": "set_value", "device": "FrontLight", "channel": 2, "value": 128}
        {"action": "set_all", "device": "Motor", "value": 200}
        {"action": "reset_errors"}
        """
        try:
            cmd = json.loads(json_str)
        except json.JSONDecodeError:
            print("[Controller] Chybný JSON:", json_str)
            return

        action = cmd.get("action")

        if action == "set_value":
            self._set_value(cmd)
        elif action == "set_all":
            self._set_all(cmd)
        elif action == "reset_errors":
            self.system.error_manager.reset_errors(lambda: True)
        else:
            print(f"[Controller] Neznámá akce: {action}")

    # -------------------- Privátní metody --------------------

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

    def _find_device(self, name: Optional[str]) -> Optional[DMXDevice]:
        for device in self.system.devices:
            if device.name == name:
                return device
        print(f"[Controller] Zařízení '{name}' nenalezeno.")
        return None

