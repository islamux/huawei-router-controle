# Huawei Connect - Quick Start Guide

## 🚀 Get Started in 60 Seconds

### 1️⃣ Install & Run

```bash
# Clone the repository
git clone https://github.com/islamux/huawei-router-controle.git
cd huawei-router-controle

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install huaweisms

# Run the application
python huawei.py
```

### 2️⃣ Configure (Optional)

Edit `huawei.py` and update:

```python
MODEM_USER = "admin"      # Your modem username
MODEM_PASS = "password"  # Your modem password
MODEM_HOST = "192.168.8.1" # Your modem IP
```

### 3️⃣ Use the Menu

```
=== HUAWEI MODEM CONTROL MENU ===
1. Device Information      # Hardware/software details
2. Connection Status       # Signal, network, connection
3. Connected Hosts         # List of connected devices
4. Recent SMS              # View SMS messages
5. Send SMS                # Send new SMS
6. Reboot Modem            # Reboot your modem
7. Show All                # All information
0. Exit                    # Quit application
===============================
```

## 📋 Common Commands Cheat Sheet

### Check Connection Status
```
Select: 2
```

### List Connected Devices
```
Select: 3
```

### View SMS Messages
```
Select: 4
Enter: 5 (for 5 messages)
```

### Send SMS
```
Select: 5
Enter: phone_number
Enter: your_message
```

### Reboot Modem
```
Select: 6
Confirm: y
```

### Exit Application
```
Select: 0
```

## 🛠️ Troubleshooting Quick Fixes

**Connection Failed?**
- Check modem IP address
- Verify username/password
- Ensure modem is powered on

**Missing Dependencies?**
```bash
pip install huaweisms
```

**Permission Issues?**
```bash
# Activate virtual environment
source venv/bin/activate
```

## 🎮 Example Workflow

### Quick Status Check
```
python huawei.py
2 → View connection status
0 → Exit
```

### Full Diagnostics
```
python huawei.py
2 → Check connection
3 → List devices  
6 → Reboot if needed
0 → Exit
```

### SMS Management
```
python huawei.py
4 → View SMS (enter quantity)
5 → Send reply
0 → Exit
```

## 📱 Supported Features

✅ **Device Information** - Hardware/software details
✅ **Connection Status** - Signal strength, network type
✅ **Connected Hosts** - List of connected devices
✅ **SMS Management** - View and send SMS
✅ **Modem Reboot** - Remote reboot capability
✅ **Interactive Menu** - Easy navigation
✅ **Colorful Output** - Attractive display

## 🔐 Security Note

For better security, use environment variables:

```bash
export MODEM_USER="your_username"
export MODEM_PASS="your_password"
export MODEM_HOST="192.168.8.1"
```

Then modify `huawei.py` to use `os.environ.get()` instead of hardcoded values.

## 🎉 Enjoy Your Huawei Connect Tool!

The interactive menu makes modem management easy and efficient!