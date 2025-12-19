# Huawei Connect - Modem Management Tool

## 🎯 Overview

Huawei Connect is a Python application for monitoring and controlling Huawei modems/routers. It provides an interactive menu system for accessing device information, connection status, connected hosts, SMS management, and more.

## 📁 Project Structure

```
huawei-connect/
├── main.py                # Main entry point
├── modem/                 # Modem-related modules
│   ├── __init__.py        # HuaweiModem class
│   ├── menu.py            # Interactive menu system
│   └── display.py         # Display functions
├── utils/                 # Utility modules
│   └── colors.py          # Color definitions
├── config.py              # Configuration settings
├── .gitignore             # Git ignore rules
├── INSTALLATION_GUIDE.md  # Installation instructions
├── QUICK_START.md         # Quick reference
└── README.md              # This file
```

## 🚀 Quick Start

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

# Configure (edit config.py or use environment variables)
# MODEM_USER="your_username"
# MODEM_PASS="your_password"
# MODEM_HOST="192.168.8.1"

# Run the application
python main.py
```

## 🎮 Features

### Interactive Menu Options:

| Option | Feature | Description |
|--------|---------|-------------|
| **1** | Device Information | Hardware/software details, serial numbers |
| **2** | Connection Status | Signal strength, network type, connection info |
| **3** | Connected Hosts | List of connected devices with details |
| **4** | Recent SMS | View SMS messages (customizable quantity) |
| **5** | Send SMS | Send new SMS messages from modem |
| **6** | Reboot Modem | Remote reboot with confirmation |
| **7** | Bandwidth Control | Set upload/download limits for devices |
| **8** | Show All | Display all information sequentially |
| **0** | Exit | Cleanly exit the application |

### Key Features:

- ✅ **Interactive Menu System** - Easy navigation
- ✅ **Colorful Output** - Attractive terminal display
- ✅ **Modular Architecture** - Clean, maintainable code
- ✅ **Error Handling** - Graceful error recovery
- ✅ **Input Validation** - Prevents invalid inputs
- ✅ **Security Features** - Confirmation for critical actions
- ✅ **Extensible Design** - Easy to add new features

## 📋 Configuration

Edit `config.py` to set your modem credentials:

```python
MODEM_USER = "admin"          # Your modem username
MODEM_PASS = "your_password"  # Your modem password
MODEM_HOST = "192.168.8.1"    # Your modem IP address
```

**For better security**, use environment variables:

```bash
export MODEM_USER="your_username"
export MODEM_PASS="your_password"
export MODEM_HOST="192.168.8.1"
```

## 🔧 Architecture

### Modular Design:

1. **`main.py`** - Entry point and main loop
2. **`modem/`** - Modem functionality
   - `__init__.py` - Core HuaweiModem class
   - `menu.py` - Interactive menu system
   - `display.py` - Display functions
3. **`utils/`** - Utility functions
   - `colors.py` - ANSI color codes
4. **`config.py`** - Configuration settings

### Benefits:

- **Separation of Concerns** - Each module has a clear responsibility
- **Easier Maintenance** - Changes are localized to specific modules
- **Better Testability** - Modules can be tested independently
- **Improved Readability** - Smaller, focused files
- **Enhanced Reusability** - Modules can be reused in other projects

## 📱 Supported Modems

Tested with:
- **Huawei B535-932a** (4G CPE)

May work with other Huawei models:
- B525, B535, B618, B715
- E5186, E5577, E5786
- Other Huawei 4G/5G routers with similar APIs

## 🛠️ Requirements

- Python 3.11+
- `huaweisms` package
- Network access to your Huawei modem
- Modem credentials

## 📚 Documentation

- **Installation Guide**: See `INSTALLATION_GUIDE.md` for detailed setup instructions
- **Quick Start**: See `QUICK_START.md` for quick reference and cheat sheet
- **API Documentation**: The `huaweisms` package provides the underlying API

## 🤝 Contributing

Contributions are welcome! The modular structure makes it easy to:

- Add new features as separate modules
- Extend existing functionality
- Improve error handling
- Add more display options
- Support additional modem models

## 📝 License

This project is for personal and educational use. Check the `huaweisms` package license for dependency terms.

## 🎉 Enjoy!

The Huawei Connect tool provides a user-friendly interface for managing your Huawei modem. The modular architecture ensures the code is maintainable and extensible for future enhancements.