#!/usr/bin/env python3
"""
Demonstration script showing the difference between old and new output formats
"""

import json
from huawei import Colors

class DemoOutput:
    def __init__(self):
        self.colors = Colors()
        
    def old_format_demo(self):
        """Show the old JSON format"""
        print("=== OLD FORMAT (JSON dumps) ===")
        sample_data = {
            "DeviceName": "B535-932a",
            "SerialNumber": "AVEUT24116001194",
            "HardwareVersion": "WL6B535M03",
            "SoftwareVersion": "2.1.0.1(H325SP3C1631)",
            "ConnectedDevices": [
                {
                    "HostName": "islamux",
                    "MacAddress": "D0:C6:37:DC:FF:87",
                    "IpAddress": "192.168.8.5"
                },
                {
                    "HostName": "S24-Ultra",
                    "MacAddress": "BC:93:07:5D:05:10",
                    "IpAddress": "192.168.8.137"
                }
            ]
        }
        print(json.dumps(sample_data, indent=2))
        
    def new_format_demo(self):
        """Show the new colorful format"""
        print(f"\n=== NEW FORMAT (Colorful & Structured) ===")
        sample_data = {
            "DeviceName": "B535-932a",
            "SerialNumber": "AVEUT24116001194",
            "HardwareVersion": "WL6B535M03",
            "SoftwareVersion": "2.1.0.1(H325SP3C1631)",
            "ConnectedDevices": [
                {
                    "HostName": "islamux",
                    "MacAddress": "D0:C6:37:DC:FF:87",
                    "IpAddress": "192.168.8.5"
                },
                {
                    "HostName": "S24-Ultra",
                    "MacAddress": "BC:93:07:5D:05:10",
                    "IpAddress": "192.168.8.137"
                }
            ]
        }
        
        # Print section header
        title = "Device Information"
        border = Colors.HEADER + "=" * (len(title) + 4) + Colors.ENDC
        print(f"\n{border}")
        print(f"{Colors.HEADER}{Colors.BOLD}  {title}  {Colors.ENDC}")
        print(border)
        
        # Print key-value pairs
        for key, value in sample_data.items():
            if isinstance(value, list):
                print(f"{Colors.OKBLUE}{key}:{Colors.ENDC}")
                for i, item in enumerate(value, 1):
                    print(f"  [{i}]")
                    for k, v in item.items():
                        print(f"    {Colors.OKBLUE}{k}:{Colors.ENDC} {Colors.OKGREEN}{v}{Colors.ENDC}")
            else:
                print(f"{Colors.OKBLUE}{key}:{Colors.ENDC} {Colors.OKGREEN}{value}{Colors.ENDC}")
        
        # Show error messages
        print(f"\n{Colors.OKBLUE}ℹ This is an info message{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ This is a success message{Colors.ENDC}")
        print(f"{Colors.FAIL}❌ This is an error message{Colors.ENDC}")

if __name__ == "__main__":
    demo = DemoOutput()
    demo.old_format_demo()
    demo.new_format_demo()