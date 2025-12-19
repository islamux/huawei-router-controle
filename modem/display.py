"""
Display module - Functions for displaying modem information

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

def display_device_info(modem):
    """Display device information"""
    modem._print_section_header("Device Information")
    info = modem.get_device_info()
    if info:
        for key, value in info.items():
            modem._print_key_value(key, value)
    else:
        modem._print_error("No device information available")

def display_connection_status(modem):
    """Display connection status"""
    modem._print_section_header("Connection Status")
    status = modem.get_status()
    if status:
        for key, value in status.items():
            modem._print_key_value(key, value)
    else:
        modem._print_error("No connection status available")

def display_connected_hosts(modem):
    """Display connected hosts"""
    modem._print_section_header("Connected Hosts")
    try:
        hosts = modem.get_connected_hosts()
        if hosts:
            for key, value in hosts.items():
                modem._print_key_value(key, value)
        else:
            modem._print_info("No connected hosts found")
    except Exception as e:
        modem._print_error(f"Could not fetch hosts: {e}")

def display_recent_sms(modem):
    """Display recent SMS messages"""
    modem._print_section_header("Recent SMS")
    try:
        qty = input(f"How many SMS messages to show? (default 5): ")
        qty = int(qty) if qty.strip() else 5
        sms = modem.get_sms_list(qty=qty)
        if sms:
            for key, value in sms.items():
                modem._print_key_value(key, value)
        else:
            modem._print_info("No SMS messages found")
    except ValueError:
        modem._print_error("Please enter a valid number")
    except Exception as e:
        modem._print_error(f"Could not fetch SMS: {e}")

def send_sms_message(modem):
    """Send an SMS message"""
    modem._print_section_header("Send SMS")
    try:
        phone_number = input("Enter phone number: ")
        message = input("Enter message: ")
        
        if phone_number and message:
            result = modem.send_sms(phone_number, message)
            if result:
                modem._print_success("SMS sent successfully!")
            else:
                modem._print_error("Failed to send SMS")
        else:
            modem._print_error("Phone number and message cannot be empty")
    except Exception as e:
        modem._print_error(f"Error sending SMS: {e}")

def reboot_modem(modem):
    """Reboot the modem"""
    modem._print_section_header("Reboot Modem")
    confirmation = input("⚠️  Are you sure you want to reboot the modem? (y/n): ")
    if confirmation.lower() == 'y':
        try:
            result = modem.reboot()
            if result:
                modem._print_success("Modem reboot initiated successfully!")
            else:
                modem._print_error("Failed to reboot modem")
        except Exception as e:
            modem._print_error(f"Error rebooting modem: {e}")
    else:
        modem._print_info("Reboot cancelled")

def display_bandwidth_control(modem):
    """Interface for setting host bandwidth limits"""
    modem._print_section_header("Bandwidth Control")
    
    try:
        hosts_data = modem.get_connected_hosts()
        if not hosts_data or 'Hosts' not in hosts_data.get('response', {}):
            modem._print_error("Could not fetch connected hosts")
            return

        hosts = hosts_data['response']['Hosts']['Host']
        if not isinstance(hosts, list):
            hosts = [hosts]

        print(f"\nSelect a device to limit:")
        for i, host in enumerate(hosts, 1):
            name = host.get('HostName', 'Unknown')
            mac = host.get('MacAddress', 'Unknown')
            ip = host.get('IpAddress', 'Unknown')
            print(f"[{i}] {name} (IP: {ip}, MAC: {mac})")

        choice = input(f"\nEnter device number (or 'c' to cancel): ")
        if choice.lower() == 'c':
            return

        idx = int(choice) - 1
        if 0 <= idx < len(hosts):
            target_host = hosts[idx]
            mac = target_host['MacAddress']
            
            print(f"\nSetting limits for {target_host.get('HostName')}")
            up_limit = input("Enter Upload Limit (KB/s, 0 for no limit): ")
            down_limit = input("Enter Download Limit (KB/s, 0 for no limit): ")
            
            up_limit = int(up_limit) if up_limit.strip() else 0
            down_limit = int(down_limit) if down_limit.strip() else 0
            
            result = modem.set_host_limit(mac, up_limit, down_limit)
            
            if result and result.get('type') == 'response':
                modem._print_success("Bandwidth limit command sent successfully!")
                modem._print_info("Note: Effect depends on modem support.")
            else:
                error_msg = result.get('error', {}).get('message', 'Unknown error') if result else "No response"
                modem._print_error(f"Failed to set limit: {error_msg}")
        else:
            modem._print_error("Invalid selection")

    except ValueError:
        modem._print_error("Invalid input. Please enter numbers.")
    except Exception as e:
        modem._print_error(f"Error in bandwidth control: {e}")

def show_all_information(modem):
    """Display all available information"""
    display_device_info(modem)
    display_connection_status(modem)
    display_connected_hosts(modem)
    display_recent_sms(modem)

def display_disconnected_devices(modem):
    """Display devices that are known but currently disconnected"""
    modem._print_section_header("Disconnected Devices")

    try:
        modem.sync_device_list()

        disconnected = modem.get_disconnected_devices()

        if not disconnected:
            modem._print_info("No disconnected devices found")
            modem._print_info("This list shows devices that have previously connected but are now offline")
            return

        print(f"\n{Colors.OKBLUE}Found {len(disconnected)} disconnected device(s):{Colors.ENDC}\n")

        for i, device in enumerate(disconnected, 1):
            name = device.get('HostName', 'Unknown')
            mac = device.get('MacAddress', 'Unknown')
            ip = device.get('IpAddress', 'Unknown')
            connection_type = device.get('ConnectionType', 'Unknown')
            first_seen = device.get('first_seen', 'Unknown')
            last_seen = device.get('last_seen', 'Unknown')

            print(f"{Colors.HEADER}[{i}] {name}{Colors.ENDC}")
            print(f"   MAC Address: {Colors.OKGREEN}{mac}{Colors.ENDC}")
            print(f"   IP Address:  {Colors.OKGREEN}{ip}{Colors.ENDC}")
            print(f"   Type:        {Colors.OKGREEN}{connection_type}{Colors.ENDC}")
            print(f"   First Seen:  {first_seen}")
            print(f"   Last Seen:   {last_seen}")
            print()

    except Exception as e:
        modem._print_error(f"Could not fetch disconnected devices: {e}")