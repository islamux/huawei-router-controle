import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms
import huaweisms.api.device
import huaweisms.api.monitoring
import json

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        url = "{}/{}".format(self.ctx.api_base_url, endpoint.lstrip('/'))
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

def show_menu():
    """Display the interactive menu"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== HUAWEI MODEM CONTROL MENU ==={Colors.ENDC}")
    print(f"{Colors.OKBLUE}1.{Colors.ENDC} Device Information")
    print(f"{Colors.OKBLUE}2.{Colors.ENDC} Connection Status")
    print(f"{Colors.OKBLUE}3.{Colors.ENDC} Connected Hosts")
    print(f"{Colors.OKBLUE}4.{Colors.ENDC} Recent SMS Messages")
    print(f"{Colors.OKBLUE}5.{Colors.ENDC} Send SMS")
    print(f"{Colors.OKBLUE}6.{Colors.ENDC} Reboot Modem")
    print(f"{Colors.OKBLUE}7.{Colors.ENDC} Bandwidth Control (Speed Limit)")
    print(f"{Colors.OKBLUE}8.{Colors.ENDC} Show All Information")
    print(f"{Colors.OKBLUE}0.{Colors.ENDC} Exit")
    print(f"{Colors.HEADER}==============================={Colors.ENDC}")

def get_user_choice():
    """Get and validate user input"""
    while True:
        try:
            choice = input(f"{Colors.OKGREEN}Enter your choice (0-7): {Colors.ENDC}")
            choice = int(choice)
            if 0 <= choice <= 8:
                return choice
            else:
                print(f"{Colors.FAIL}❌ Please enter a number between 0 and 8{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}❌ Please enter a valid number{Colors.ENDC}")

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
        qty = input(f"{Colors.OKBLUE}How many SMS messages to show? (default 5): {Colors.ENDC}")
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
        phone_number = input(f"{Colors.OKBLUE}Enter phone number: {Colors.ENDC}")
        message = input(f"{Colors.OKBLUE}Enter message: {Colors.ENDC}")
        
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
    confirmation = input(f"{Colors.WARNING}⚠️  Are you sure you want to reboot the modem? (y/n): {Colors.ENDC}")
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

        print(f"\n{Colors.BOLD}Select a device to limit:{Colors.ENDC}")
        for i, host in enumerate(hosts, 1):
            name = host.get('HostName', 'Unknown')
            mac = host.get('MacAddress', 'Unknown')
            ip = host.get('IpAddress', 'Unknown')
            print(f"{Colors.OKBLUE}[{i}]{Colors.ENDC} {name} (IP: {ip}, MAC: {mac})")

        choice = input(f"\n{Colors.OKBLUE}Enter device number (or 'c' to cancel): {Colors.ENDC}")
        if choice.lower() == 'c':
            return

        idx = int(choice) - 1
        if 0 <= idx < len(hosts):
            target_host = hosts[idx]
            mac = target_host['MacAddress']
            
            print(f"\nSetting limits for {Colors.BOLD}{target_host.get('HostName')}{Colors.ENDC}")
            up_limit = input(f"{Colors.OKBLUE}Enter Upload Limit (KB/s, 0 for no limit): {Colors.ENDC}")
            down_limit = input(f"{Colors.OKBLUE}Enter Download Limit (KB/s, 0 for no limit): {Colors.ENDC}")
            
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

if __name__ == "__main__":
    # Configuration - adjust if necessary
    MODEM_USER = "admin"
    MODEM_PASS = "islamux269733"
    MODEM_HOST = "192.168.8.1"

    modem = HuaweiModem(MODEM_USER, MODEM_PASS, MODEM_HOST)
    
    if modem.connect():
        modem._print_success("Authenticated Successfully")
        
        while True:
            show_menu()
            choice = get_user_choice()
            
            if choice == 0:
                modem._print_info("Goodbye!")
                break
            elif choice == 1:
                display_device_info(modem)
            elif choice == 2:
                display_connection_status(modem)
            elif choice == 3:
                display_connected_hosts(modem)
            elif choice == 4:
                display_recent_sms(modem)
            elif choice == 5:
                send_sms_message(modem)
            elif choice == 6:
                reboot_modem(modem)
            elif choice == 7:
                display_bandwidth_control(modem)
            elif choice == 8:
                show_all_information(modem)
            
            # Ask if user wants to continue
            if choice != 0:
                continue_choice = input(f"\n{Colors.OKBLUE}Press Enter to continue or 'q' to quit...{Colors.ENDC}")
                if continue_choice.lower() == 'q':
                    modem._print_info("Goodbye!")
                    break
    else:
        modem._print_error("Failed to initialize modem connection")
