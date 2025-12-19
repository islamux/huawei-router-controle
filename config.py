"""
Configuration module - Centralized configuration settings
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