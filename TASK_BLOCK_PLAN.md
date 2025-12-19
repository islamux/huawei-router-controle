# Plan: Add Task Block Client Feature

## Objective
Add functionality to block/unblock specific client devices from accessing the modem network, providing network access control capabilities.

## Analysis
Based on the existing codebase structure:
- The application already tracks connected and disconnected devices
- Huawei modems typically support device blocking via MAC address filtering
- The huaweisms API can be used to manage device access control
- Need to integrate with existing device tracking system

## Implementation Approach

### Option 1: MAC Address Blocking via API (RECOMMENDED)
Use huaweisms API to manage MAC address blacklist/whitelist for network access control.

**Steps:**
1. Add methods to retrieve current MAC filter settings
2. Add methods to block/unblock devices by MAC address
3. Add menu option to view blocked devices
4. Add menu option to block a device
5. Add menu option to unblock a device
6. Integrate with device tracker for easy device selection

### Option 2: Manual Configuration Interface
Provide instructions for manual modem configuration.

**Decision: Go with Option 1** - Direct API control provides better user experience and automation.

## Detailed Implementation Steps

### Step 1: Extend HuaweiModem Class
Add methods to `modem/__init__.py`:
- `get_blocked_devices()` - Retrieve list of blocked MAC addresses
- `block_device(mac_address)` - Add MAC to blocked list
- `unblock_device(mac_address)` - Remove MAC from blocked list
- `is_device_blocked(mac_address)` - Check if device is blocked

### Step 2: Add Display Functions
Create functions in `modem/display.py`:
- `display_blocked_devices()` - Show all currently blocked devices
- `display_block_device_menu()` - Interactive menu for blocking devices
- `display_unblock_device_menu()` - Interactive menu for unblocking devices

### Step 3: Update Configuration
Add new menu options in `config.py`:
```python
10: "View Blocked Devices"
11: "Block a Device"
12: "Unblock a Device"
```

### Step 4: Update Menu Handler
Modify `main.py` to handle new menu options:
- Add imports for new display functions
- Add cases for choices 10, 11, 12

### Step 5: Integration with Device Tracker
Enhance device tracker to show blocking status:
- Add `is_blocked` field to device records
- Sync blocking status with device list
- Show blocked status in disconnected devices view

## Files to Modify

1. **Modify:** `modem/__init__.py` - Add blocking control methods
2. **Modify:** `modem/display.py` - Add blocking-related display functions
3. **Modify:** `config.py` - Add new menu options (10, 11, 12)
4. **Modify:** `main.py` - Add menu handlers for blocking features
5. **Modify:** `modem/device_tracker.py` - Add blocking status tracking

## Technical Implementation Details

### MAC Address Blocking via huaweisms API
The huaweisms library provides methods for managing MAC filters:
- `api.mac_filterwitch()` - Enable/disable MAC filtering
- `api.get_mac_filter_settings()` - Get current filter settings
- `api.set_mac_filter_settings()` - Update filter settings

### Device Tracking Enhancement
Update `known_devices.json` structure:
```json
{
  "devices": [
    {
      "MacAddress": "XX:XX:XX:XX:XX:XX",
      "HostName": "Device Name",
      "IpAddress": "192.168.x.x",
      "ConnectionType": "WiFi/Ethernet",
      "is_connected": true,
      "is_blocked": false,
      "first_seen": "timestamp",
      "last_seen": "timestamp"
    }
  ],
  "last_updated": "timestamp"
}
```

### API Endpoints Reference
Based on huaweisms library capabilities:
- `api.mac_filterwitch` - Control MAC filtering on/off
- `api.get_mac_filter_settings` - Retrieve filter configuration
- `api.set_mac_filter_settings` - Modify filter settings

## User Interface Flow

### Menu Option 10: View Blocked Devices
1. Fetch current blocked devices from modem
2. Display formatted list with MAC addresses and device info
3. Show count of blocked vs total devices
4. Option to return to main menu

### Menu Option 11: Block a Device
1. Show list of currently connected devices
2. Allow user to select device by number or enter MAC address
3. Confirm blocking action
4. Block device via API
5. Update local device tracker
6. Show success/error message

### Menu Option 12: Unblock a Device
1. Show list of blocked devices
2. Allow user to select device by number or enter MAC address
3. Confirm unblocking action
4. Unblock device via API
5. Update local device tracker
6. Show success/error message

## Error Handling

- Validate MAC address format before API calls
- Handle API errors gracefully with user-friendly messages
- Check device existence before attempting to block/unblock
- Verify modem supports MAC filtering feature

## Benefits

✅ Complete network access control
✅ Easy device management via MAC address
✅ Integration with existing device tracking
✅ Visual feedback on blocking status
✅ Persistent blocking across modem restarts
✅ Support for both connected and disconnected devices

## Security Considerations

- MAC addresses can be spoofed, but this provides basic access control
- Blocked devices cannot access network even with correct WiFi password
- Only admin users should have access to blocking features
- Log all blocking/unblocking actions for audit trail

## Testing

After implementation:
1. Test blocking a connected device - verify it loses network access
2. Test unblocking a device - verify it regains network access
3. Test blocking a disconnected device - verify it remains blocked when connecting
4. Test viewing blocked devices list
5. Verify device tracker updates blocking status correctly
6. Test with multiple devices and verify isolation

## Estimated Complexity
- **Time:** ~2-3 hours
- **Difficulty:** Medium-High
- **Risk:** Medium (requires API testing and verification)
- **Dependencies:** huaweisms library MAC filter support

## Next Steps After Implementation
- Add bandwidth control per blocked device
- Add scheduling for temporary blocking
- Add email/SMS notifications for blocked devices
- Add MAC address range blocking
