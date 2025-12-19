"""
Main entry point for Huawei Connect application
"""

from modem import HuaweiModem
from modem.menu import show_menu, get_user_choice, get_continue_choice
from modem.display import (
    display_device_info, display_connection_status, 
    display_connected_hosts, display_recent_sms,
    send_sms_message, reboot_modem,
    display_bandwidth_control, show_all_information
)
from config import MODEM_USER, MODEM_PASS, MODEM_HOST

def main():
    """Main application entry point"""
    
    # Create modem instance with configuration
    modem = HuaweiModem(MODEM_USER, MODEM_PASS, MODEM_HOST)
    
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