"""
Configuration module - Centralized configuration settings

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

# Default configuration
MODEM_USER = "admin"
MODEM_PASS = None  # Password must be provided via command line for security
MODEM_HOST = "192.168.8.1"

# Menu options
MENU_OPTIONS = {
    1: "Device Information",
    2: "Connection Status",
    3: "Connected Hosts",
    4: "Recent SMS Messages",
    5: "Send SMS",
    6: "Reboot Modem",
    7: "Bandwidth Control (Speed Limit)",
    8: "Show All Information",
    0: "Exit"
}