# Huawei Connect - Installation & Usage Guide

## 🎯 Overview

This guide provides step-by-step instructions for installing and running the Huawei Connect tool, which allows you to monitor and control your Huawei modem/router.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11 or higher** installed on your system
- **pip** (Python package manager) installed
- **A Huawei modem/router** (tested with B535-932a)
- **Network access** to your modem (usually at `192.168.8.1`)
- **Modem credentials** (default: username=`admin`, password=`admin` or your custom password)

## 🔧 Step 1: Clone the Repository

```bash
# Clone the repository to your local machine
git clone https://github.com/islamux/huawei-router-controle.git

# Navigate to the project directory
cd huawei-router-controle
```

## 🐍 Step 2: Set Up Python Virtual Environment

```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## 📦 Step 3: Install Required Dependencies

```bash
# Install the required Python packages
pip install huaweisms
```

**Note:** The `huaweisms` package provides the API client for communicating with Huawei modems.

## ⚙️ Step 4: Configure the Application

The application now supports command-line arguments for better security. You can:

### Option 1: Use Command Line Arguments (Recommended)

```bash
python main.py --user admin --password your_password --host 192.168.8.1
```

### Option 2: Set Defaults in config.py

Edit `config.py` for default values (password still required via command line):

```python
# Default configuration
MODEM_USER = "admin"          # Default username
MODEM_HOST = "192.168.8.1"    # Default host
```

**Important Security Note:** The password must be provided via command line for security. This prevents storing sensitive credentials in files or version control.
- Using `.env` files with proper security

## 🚀 Step 5: Run the Application

```bash
# Run the Huawei Connect tool with password
python main.py --password your_password

# Or with all options:
python main.py --user admin --password your_password --host 192.168.8.1

# Short form:
python main.py -u admin -p your_password -H 192.168.8.1
```

**Note:** The password is now required via command line for better security.

## 🎮 Step 6: Using the Interactive Menu

Once the application starts successfully, you'll see the interactive menu:

```
=== HUAWEI MODEM CONTROL MENU ===
1. Device Information
2. Connection Status  
3. Connected Hosts
4. Recent SMS Messages
5. Send SMS
6. Reboot Modem
7. Show All Information
0. Exit
===============================
```

### Menu Options Explained:

| Option | Description | What You'll See |
|--------|-------------|-----------------|
| **1** | Device Information | Hardware/software details, serial numbers, versions |
| **2** | Connection Status | Signal strength, network type, connection info |
| **3** | Connected Hosts | List of devices connected to your modem |
| **4** | Recent SMS | SMS messages stored on the modem (customizable quantity) |
| **5** | Send SMS | Send new SMS messages from the modem |
| **6** | Reboot Modem | Reboot your modem (requires confirmation) |
| **7** | Show All | Display all information sequentially |
| **0** | Exit | Cleanly exit the application |

## 📱 Example Usage Scenarios

### Scenario 1: Quick Status Check
```
1. Run: python huawei.py
2. Select: 2 (Connection Status)
3. View: Signal strength, network type, etc.
4. Select: 0 (Exit)
```

### Scenario 2: Troubleshooting Connection
```
1. Run: python huawei.py
2. Select: 3 (Connected Hosts) - Check connected devices
3. Select: 2 (Connection Status) - Check signal strength
4. Select: 6 (Reboot Modem) - If needed
5. Confirm reboot with 'y'
```

### Scenario 3: SMS Management
```
1. Run: python huawei.py
2. Select: 4 (Recent SMS) - View messages
3. Enter: 5 (when asked for quantity)
4. Select: 5 (Send SMS) - Send reply
5. Enter: Phone number and message
6. Select: 0 (Exit)
```

## 🔐 Security Best Practices

### For Production Use:

1. **Use Environment Variables:**
   ```bash
   export MODEM_USER="your_username"
   export MODEM_PASS="your_password"
   export MODEM_HOST="192.168.8.1"
   ```

2. **Create a `.env` file:**
   ```env
   MODEM_USER=your_username
   MODEM_PASS=your_password  
   MODEM_HOST=192.168.8.1
   ```

3. **Add `.env` to `.gitignore`:**
   ```gitignore
   .env
   ```

## 🛠️ Troubleshooting

### Common Issues and Solutions:

**Issue: Connection Failed**
- **Cause:** Wrong credentials or modem IP
- **Solution:** Verify modem IP and credentials in configuration

**Issue: Could not fetch hosts/SMS**
- **Cause:** Feature not supported by your modem model
- **Solution:** Check modem compatibility or update firmware

**Issue: ModuleNotFoundError**
- **Cause:** Missing dependencies
- **Solution:** Run `pip install huaweisms`

**Issue: Permission denied**
- **Cause:** Virtual environment not activated
- **Solution:** Run `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)

## 📱 Supported Modem Models

The tool has been tested with:
- **Huawei B535-932a** (4G CPE)

May work with other Huawei models using the same API:
- B525, B535, B618, B715
- E5186, E5577, E5786
- Other Huawei 4G/5G routers

## 🔄 Updating the Application

```bash
# Pull the latest changes
git pull origin main

# Update dependencies
pip install --upgrade huaweisms
```

## 📝 License

This project is for personal use. Check the license of the `huaweisms` package for dependency licensing.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## 📞 Support

For issues or questions:
- Check the GitHub issues page
- Verify your modem model compatibility
- Ensure you're using the correct credentials

## 🎉 Enjoy Your Huawei Connect Tool!

The interactive menu makes it easy to monitor and control your Huawei modem. Whether you need to check connection status, view connected devices, or send SMS messages, this tool provides a user-friendly interface for all your modem management needs.