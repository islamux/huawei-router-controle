"""
Modem module - Main HuaweiModem class and core functionality

Copyright (C) 2025 Islamux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms
import huaweisms.api.device
import huaweisms.api.monitoring
import huaweisms.api.common
from utils.colors import Colors
from modem.device_tracker import sync_devices, get_disconnected_devices, get_known_devices

class HuaweiModem:
    def __init__(self, username="admin", password="password", modem_host="192.168.8.1"):
        self.username = username
        self.password = password
        self.modem_host = modem_host
        self.ctx = None

    def connect(self):
        """Authenticates with the modem."""
        try:
            self.ctx = huaweisms.api.user.quick_login(
                self.username, 
                self.password, 
                modem_host=self.modem_host
            )
            return True
        except Exception as e:
            self._print_error(f"Connection failed: {e}")
            return False

    def get_connected_hosts(self):
        """Returns a list of connected devices."""
        if not self.ctx:
            return None
        return huaweisms.api.wlan.get_connected_hosts(self.ctx)

    def get_device_info(self):
        """Returns hardware and software information about the modem."""
        if not self.ctx:
            return None
        return huaweisms.api.device.information(self.ctx)

    def get_status(self):
        """Returns monitoring status (signal, network type, etc.)."""
        if not self.ctx:
            return None
        return huaweisms.api.monitoring.status(self.ctx)

    def get_sms_list(self, qty=10):
        """Returns the latest SMS messages."""
        if not self.ctx:
            return None
        return huaweisms.api.sms.get_sms(self.ctx, qty=qty)

    def send_sms(self, phone_number, message):
        """Sends an SMS message."""
        if not self.ctx:
            return None
        return huaweisms.api.sms.send_sms(self.ctx, phone_number, message)

    def reboot(self):
        """Reboots the modem."""
        if not self.ctx:
            return None
        return huaweisms.api.device.reboot(self.ctx)

    def _send_custom_xml(self, endpoint, xml_data):
        """Sends a custom XML payload to a specified endpoint."""
        if not self.ctx:
            return None
        url = "{}/{}.".format(self.ctx.api_base_url, endpoint.lstrip('/'))
        headers = {
            "__RequestVerificationToken": self.ctx.token,
        }
        return huaweisms.api.common.post_to_url(
            url, xml_data, self.ctx, additional_headers=headers
        )

    def set_host_limit(self, mac_address, upload_speed, download_speed):
        """
        Sets speed limits for a specific device.
        Speeds are in KB/s. 0 means no limit.
        Note: This endpoint might vary by firmware.
        """
        xml_data = """<?xml version="1.0" encoding="UTF-8"?>
        <request>
            <Status>1</Status>
            <ID></ID>
            <Mac>{}</Mac>
            <UploadRate>{}</UploadRate>
            <DownloadRate>{}</DownloadRate>
        </request>""".format(mac_address, upload_speed, download_speed)
        
        # We try a common qos-setup endpoint first
        return self._send_custom_xml("qos/qos-setup", xml_data)

    def _print_section_header(self, title):
        """Print a formatted section header"""
        border = Colors.HEADER + "=" * (len(title) + 4) + Colors.ENDC
        print(f"\n{border}")
        print(f"{Colors.HEADER}{Colors.BOLD}  {title}  {Colors.ENDC}")
        print(border)

    def _print_key_value(self, key, value, indent=0):
        """Print a key-value pair with proper formatting"""
        indent_str = " " * indent
        if isinstance(value, dict):
            print(f"{indent_str}{Colors.OKBLUE}{key}:{Colors.ENDC}")
            for k, v in value.items():
                self._print_key_value(k, v, indent + 2)
        elif isinstance(value, list):
            print(f"{indent_str}{Colors.OKBLUE}{key}:{Colors.ENDC}")
            for i, item in enumerate(value, 1):
                if isinstance(item, dict):
                    print(f"{indent_str}  [{i}]")
                    for k, v in item.items():
                        self._print_key_value(k, v, indent + 4)
                else:
                    self._print_key_value(f"[{i}]", item, indent + 2)
        else:
            print(f"{indent_str}{Colors.OKBLUE}{key}:{Colors.ENDC} {Colors.OKGREEN}{value}{Colors.ENDC}")

    def _print_error(self, message):
        """Print an error message in red"""
        print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

    def _print_success(self, message):
        """Print a success message in green"""
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

    def _print_info(self, message):
        """Print an info message in blue"""
        print(f"{Colors.OKBLUE}ℹ {message}{Colors.ENDC}")

    def sync_device_list(self):
        """Sync known devices with currently connected hosts"""
        current_hosts = self.get_connected_hosts()
        sync_devices(current_hosts)

    def get_disconnected_devices(self):
        """
        Get list of devices that are known but currently disconnected.
        Returns list of device dictionaries.
        """
        return get_disconnected_devices()

    def get_known_devices(self):
        """Get all known devices that have ever connected"""
        return get_known_devices()