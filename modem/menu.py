"""
Menu module - Interactive menu system and user interface

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

from utils.colors import Colors
from config import MENU_OPTIONS

def show_menu():
    """Display the interactive menu"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== HUAWEI MODEM CONTROL MENU ==={Colors.ENDC}")
    
    for option_num, option_text in MENU_OPTIONS.items():
        if option_num == 0:  # Exit option
            print(f"{Colors.OKBLUE}{option_num}.{Colors.ENDC} {option_text}")
        else:
            print(f"{Colors.OKBLUE}{option_num}.{Colors.ENDC} {option_text}")
    
    print(f"{Colors.HEADER}==============================={Colors.ENDC}")

def get_user_choice():
    """Get and validate user input"""
    max_option = max(MENU_OPTIONS.keys())
    
    while True:
        try:
            choice = input(f"{Colors.OKGREEN}Enter your choice (0-{max_option}): {Colors.ENDC}")
            choice = int(choice)
            if 0 <= choice <= max_option:
                return choice
            else:
                print(f"{Colors.FAIL}❌ Please enter a number between 0 and {max_option}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}❌ Please enter a valid number{Colors.ENDC}")

def get_continue_choice():
    """Ask user if they want to continue"""
    continue_choice = input(f"\n{Colors.OKBLUE}Press Enter to continue or 'q' to quit...{Colors.ENDC}")
    return continue_choice.lower() == 'q'