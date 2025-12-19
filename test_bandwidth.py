#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock, patch
from huawei import HuaweiModem, display_bandwidth_control, Colors

class TestBandwidthControl(unittest.TestCase):
    def setUp(self):
        self.modem = HuaweiModem()
        self.modem.ctx = MagicMock()
        self.modem.ctx.api_base_url = "http://192.168.8.1/api"
        self.modem.ctx.token = "fake_token"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_bandwidth_control_logic(self, mock_print, mock_input):
        # Mocking get_connected_hosts response
        self.modem.get_connected_hosts = MagicMock(return_value={
            'type': 'response',
            'response': {
                'Hosts': {
                    'Host': [
                        {'HostName': 'Device1', 'IpAddress': '192.168.8.10', 'MacAddress': 'AA:BB:CC:DD:EE:FF'},
                        {'HostName': 'Device2', 'IpAddress': '192.168.8.11', 'MacAddress': '11:22:33:44:55:66'}
                    ]
                }
            }
        })

        # Mock inputs: select device 1, upload 100, download 200
        mock_input.side_effect = ['1', '100', '200']

        # Mock _send_custom_xml to verify the payload
        self.modem._send_custom_xml = MagicMock(return_value={'type': 'response'})

        # Run the UI function
        display_bandwidth_control(self.modem)

        # Verify _send_custom_xml was called with correct data
        args, kwargs = self.modem._send_custom_xml.call_args
        endpoint, xml_payload = args
        
        self.assertEqual(endpoint, "qos/qos-setup")
        self.assertIn("AA:BB:CC:DD:EE:FF", xml_payload)
        self.assertIn("<UploadRate>100</UploadRate>", xml_payload)
        self.assertIn("<DownloadRate>200</DownloadRate>", xml_payload)
        
        print(f"\n{Colors.OKGREEN}✓ Bandwidth control logic test passed!{Colors.ENDC}")

if __name__ == "__main__":
    unittest.main()
