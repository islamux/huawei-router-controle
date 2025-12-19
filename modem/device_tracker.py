"""
Device Tracker module - Track and manage known devices

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

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

KNOWN_DEVICES_FILE = "known_devices.json"

def load_known_devices() -> Dict:
    """Load known devices from JSON file"""
    if os.path.exists(KNOWN_DEVICES_FILE):
        try:
            with open(KNOWN_DEVICES_FILE, 'r') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            pass

    return {
        "devices": [],
        "last_updated": None
    }

def save_known_devices(data: Dict) -> bool:
    """Save known devices to JSON file"""
    try:
        data["last_updated"] = datetime.now().isoformat()
        with open(KNOWN_DEVICES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        return False

def sync_devices(current_hosts: Optional[Dict]) -> Dict:
    """
    Sync known devices with currently connected hosts
    Returns updated known devices data
    """
    data = load_known_devices()
    known_devices = data.get("devices", [])

    if not current_hosts or 'response' not in current_hosts:
        return data

    try:
        hosts = current_hosts['response'].get('Hosts', {}).get('Host', [])
        if not hosts:
            return data

        if not isinstance(hosts, list):
            hosts = [hosts]

        current_macs = set()
        current_time = datetime.now().isoformat()

        for host in hosts:
            mac = host.get('MacAddress', '').upper()
            if not mac:
                continue

            current_macs.add(mac)

            existing_device = next(
                (d for d in known_devices if d.get('MacAddress', '').upper() == mac),
                None
            )

            if existing_device:
                existing_device['HostName'] = host.get('HostName', existing_device.get('HostName', 'Unknown'))
                existing_device['IpAddress'] = host.get('IpAddress', existing_device.get('IpAddress', 'Unknown'))
                existing_device['ConnectionType'] = host.get('ConnectionType', existing_device.get('ConnectionType', 'Unknown'))
                existing_device['is_connected'] = True
                existing_device['last_seen'] = current_time
            else:
                known_devices.append({
                    'MacAddress': mac,
                    'HostName': host.get('HostName', 'Unknown'),
                    'IpAddress': host.get('IpAddress', 'Unknown'),
                    'ConnectionType': host.get('ConnectionType', 'Unknown'),
                    'is_connected': True,
                    'first_seen': current_time,
                    'last_seen': current_time
                })

        for device in known_devices:
            mac = device.get('MacAddress', '').upper()
            if mac not in current_macs and device.get('is_connected', False):
                device['is_connected'] = False
                device['last_disconnected'] = current_time

        data["devices"] = known_devices
        save_known_devices(data)

    except (KeyError, TypeError):
        pass

    return data

def get_disconnected_devices() -> List[Dict]:
    """
    Get list of devices that are known but currently disconnected
    Returns list of device dictionaries
    """
    data = load_known_devices()
    devices = data.get("devices", [])

    disconnected = [d for d in devices if not d.get('is_connected', False)]

    disconnected.sort(key=lambda x: x.get('last_seen', ''), reverse=True)

    return disconnected

def get_known_devices() -> List[Dict]:
    """Get all known devices"""
    data = load_known_devices()
    return data.get("devices", [])

def clear_device_history() -> bool:
    """Clear all device history"""
    data = {
        "devices": [],
        "last_updated": datetime.now().isoformat()
    }
    return save_known_devices(data)
