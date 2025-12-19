# Plan: Add "List All Devices Not Connected" Feature

## Objective
Add a new menu option to display devices that are NOT currently connected to the Huawei modem.

## Analysis
After exploring the codebase, I found that:
- The application currently displays "Connected Hosts" (option 3)
- The `get_connected_hosts()` method retrieves currently connected devices via huaweisms API
- The huaweisms API doesn't provide a direct way to get "disconnected" or historical devices
- We need to implement a tracking mechanism for known devices

## Implementation Approach

### Option 1: Device Tracking with Local Database (RECOMMENDED)
Create a local JSON file to track all devices that have ever connected, then compare with currently connected devices.

**Steps:**
1. Create `known_devices.json` file to store device history
2. Add method to `HuaweiModem` class to sync and track devices
3. Add method to get disconnected devices (in known_devices but not currently connected)
4. Add new menu option "9. List All Devices Not Connected"
5. Add display function for disconnected devices
6. Update menu handler in main.py

### Option 2: Simple Currently Disconnected Display
Show devices that were last seen connected but are currently offline based on recent scan data.

**Steps:**
1. Cache last connected hosts data
2. Compare current hosts with cached data
3. Display devices in cache but not in current list

**Decision: Go with Option 1** - More robust and provides complete device history tracking.

## Detailed Implementation Steps

### Step 1: Create Device Tracking Module
- Create `modem/device_tracker.py`
- Implement functions to:
  - Load known devices from JSON
  - Save known devices to JSON
  - Sync with current connected devices
  - Get disconnected devices list

### Step 2: Extend HuaweiModem Class
- Add `device_tracker` instance variable
- Add `sync_device_list()` method to update known devices
- Add `get_disconnected_devices()` method to get devices not currently connected

### Step 3: Add Display Function
- Create `display_disconnected_devices()` in `modem/display.py`
- Format output similar to `display_connected_hosts()`
- Show device details: Name, MAC, IP (if known), last seen time

### Step 4: Update Configuration
- Add new menu option in `config.py`:
  ```python
  9: "List All Devices Not Connected"
  ```

### Step 5: Update Menu Handler
- Import new display function in `main.py`
- Add case for choice == 9

### Step 6: Create Known Devices File
- Initialize `known_devices.json` with empty structure:
  ```json
  {
    "devices": [],
    "last_updated": "timestamp"
  }
  ```

## Files to Modify

1. **New File:** `modem/device_tracker.py` - Device tracking logic
2. **Modify:** `modem/__init__.py` - Add tracking methods
3. **Modify:** `modem/display.py` - Add display function
4. **Modify:** `config.py` - Add menu option
5. **Modify:** `main.py` - Add menu handler
6. **New File:** `known_devices.json` - Device database (created automatically)

## Benefits

✅ Complete device history tracking
✅ Ability to see all devices that have ever connected
✅ Clear identification of currently disconnected devices
✅ Persistent storage across application restarts
✅ Extensible for future features (device management, alerts, etc.)

## Testing

After implementation:
1. Run application and connect to modem
2. Check "Connected Hosts" to see current devices
3. Check "List All Devices Not Connected" to see tracked but disconnected devices
4. Verify known_devices.json is created and updated
5. Test device tracking across multiple sessions

## Estimated Complexity
- **Time:** ~1-2 hours
- **Difficulty:** Medium
- **Risk:** Low (additive feature, no breaking changes)
