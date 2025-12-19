"""
Huawei Connect - Main entry point

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

import argparse
from modem import HuaweiModem
from modem.menu import show_menu, get_user_choice, get_continue_choice
from modem.display import (
    display_device_info, display_connection_status, 
    display_connected_hosts, display_recent_sms,
    send_sms_message, reboot_modem,
    display_bandwidth_control, show_all_information
)
from config import MODEM_USER, MODEM_PASS, MODEM_HOST

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Huawei Connect - Modem Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py --user admin --password mypassword
  python main.py --host 192.168.8.1 --user admin --password mypassword
  python main.py -u admin -p mypassword -h 192.168.8.1
        '''
    )
    
    parser.add_argument('-u', '--user', 
                        help='Modem username (default: admin)',
                        default=MODEM_USER)
    parser.add_argument('-p', '--password',
                        help='Modem password (required)',
                        required=True)
    parser.add_argument('-H', '--host',
                        help='Modem host/IP address (default: 192.168.8.1)',
                        default=MODEM_HOST)
    parser.add_argument('--version', action='version',
                        version='%(prog)s 1.0.0',
                        help='Show version information')
    
    return parser.parse_args()

def main():
    """Main application entry point"""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Create modem instance with configuration
    modem = HuaweiModem(args.user, args.password, args.host)
    
    # Connect to modem
    if not modem.connect():
        modem._print_error("Failed to initialize modem connection")
        return
    
    # Show success message
    modem._print_success("Authenticated Successfully")
    
    # Main application loop
    while True:
        show_menu()
        choice = get_user_choice()
        
        # Handle user choice
        if choice == 0:  # Exit
            modem._print_info("Goodbye!")
            break
        
        elif choice == 1:  # Device Information
            display_device_info(modem)
        
        elif choice == 2:  # Connection Status
            display_connection_status(modem)
        
        elif choice == 3:  # Connected Hosts
            display_connected_hosts(modem)
        
        elif choice == 4:  # Recent SMS
            display_recent_sms(modem)
        
        elif choice == 5:  # Send SMS
            send_sms_message(modem)
        
        elif choice == 6:  # Reboot Modem
            reboot_modem(modem)
        
        elif choice == 7:  # Bandwidth Control
            display_bandwidth_control(modem)
        
        elif choice == 8:  # Show All
            show_all_information(modem)
        
        # Ask if user wants to continue
        if get_continue_choice():
            modem._print_info("Goodbye!")
            break

if __name__ == "__main__":
    main()