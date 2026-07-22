<div align="center">
  <a href="https://github.com/wolf-intelligence-pk/WOLF-EYE">
    <img src="logo.png" alt="WOLF-EYE" border="0" width="200" />
  </a>

  # 🐺 WOLF-EYE v1.0 - Advanced Reconnaissance Framework
  
  ![Version](https://img.shields.io/badge/WOLF--EYE-V1.0-red?style=for-the-badge&logo=wolframlanguage&logoColor=white)
  ![Version](https://img.shields.io/badge/Version-2.0_Enhanced-blue?style=for-the-badge)
  ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20macOS-lightgrey?style=for-the-badge&logo=linux&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
  ![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python&logoColor=white)
  
  *Advanced Browser-Based Information Gathering & Geolocation Framework*
</div>

---

## 📊 Architecture Overview

```mermaid
graph TB
    A[WOLF-EYE Framework] --> B[Core Engine]
    A --> C[Web Server]
    A --> D[Data Collection]
    A --> E[Notification System]
    
    B --> B1[Python Backend]
    B --> B2[PHP Server]
    B --> B3[Template Engine]
    
    C --> C1[Local Hosting]
    C --> C2[Port Management]
    C --> C3[SSL/HTTP Handling]
    
    D --> D1[Device Info]
    D --> D2[Geolocation]
    D --> D3[IP Intelligence]
    D --> D4[CSV Logging]
    D --> D5[KML Export]
    
    E --> E1[Telegram Bot]
    E --> E2[Discord Webhook]
    E --> E3[Custom Webhooks]
```


## 🎯 Features Matrix

```mermaid
mindmap
  root((WOLF-EYE))
    Information Gathering
      Device Information
        OS & Platform
        CPU & RAM
        GPU Details
        Screen Resolution
        Browser Fingerprint
      Network Intelligence
        Public IP
        ISP Details
        Organization
        Continent & Country
      Geolocation
        Latitude/Longitude
        Accuracy
        Altitude
        Speed & Direction
    Data Management
      CSV Export
      KML Generation
      Google Maps Integration
      Auto-Save
    Notifications
      Telegram Bot
      Discord Webhooks
      Custom Webhooks
      Real-time Alerts
    Templates
      Multiple Designs
      Custom CSS/JS
      Responsive UI
```


## 🚀 Installation Process

```mermaid
graph LR
    A[Clone Repository] --> B[Run Install Script]
    B --> C{OS Detection}
    C -->|Debian/Ubuntu| D[apt-get install]
    C -->|Fedora| E[dnf install]
    C -->|Arch| F[pacman install]
    C -->|Termux| G[pkg install]
    
    D --> H[Dependencies]
    E --> H
    F --> H
    G --> H
    
    H --> I[Python Packages]
    I --> J[PHP Setup]
    J --> K[Installation Complete]
    K --> L[Auto-Launch WOLF-EYE]
```

## 💻 Quick Start

### Clone the repository
```
git clone https://github.com/wolf-intelligence-pk/WOLF-EYE.git
cd WOLF-EYE
```
### Make install script executable
```
chmod +x install.sh
```
### Run installation (auto-detects OS and launches WOLF-EYE)

```
./install.sh
```


## 🎮 Usage Examples


### Basic usage
```
python3 wolf-eye.py
```
### Specify KML output file
```
python3 wolf-eye.py -k output_filename
```
### Use specific template
```
python3 wolf-eye.py -t 0
```

### Set custom port
```
python3 wolf-eye.py -p 8080
```

### Enable Telegram notifications
```
python3 wolf-eye.py -tg "token:chatId"
```

### Enable webhook notifications
```
python3 wolf-eye.py -wh "https://webhook.url"
```

### Check for updates
```
python3 wolf-eye.py -u
```

### Display version
```
python3 wolf-eye.py -v
```

### Disable HTTPS redirection (testing)
```
python3 wolf-eye.py -d true
```

## 📋 Command Line Arguments

| Argument | Flag | Description | Example |
|----------|------|-------------|---------|
| KML Output | `-k` `--kml` | KML filename for Google Earth export | `-k target_location` |
| Port | `-p` `--port` | Web server port (Default: 8080) | `-p 4444` |
| Template | `-t` `--template` | Template number to load | `-t 0` |
| Telegram | `-tg` `--telegram` | Telegram bot token:chatId | `-tg "123456:ABC-DEF"` |
| Webhook | `-wh` `--webhook` | Webhook URL for notifications | `-wh "https://discord.com/api/webhooks/..."` |
| Update | `-u` `--update` | Check for latest version | `-u` |
| Version | `-v` `--version` | Print current version | `-v` |
| Debug HTTP | `-d` `--debugHTTP` | Disable HTTPS redirection | `-d true` |

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PORT` | Web server port | `export PORT=4444` |
| `TELEGRAM` | Telegram bot credentials | `export TELEGRAM="token:chatId"` |
| `WEBHOOK` | Webhook URL | `export WEBHOOK="https://..."` |
| `DEBUG_HTTP` | Debug mode flag | `export DEBUG_HTTP=1` |
| `TEMPLATE` | Template number | `export TEMPLATE=0` |

## 🔧 Data Collection Pipeline

```mermaid
graph TD
    A[Client Visit] --> B{Location Permission}
    B -->|Granted| C[GPS Coordinates]
    B -->|Denied| D[IP-based Location]
    
    C --> E[Device Info Collection]
    D --> E
    
    E --> F[OS Detection]
    E --> G[Browser Fingerprinting]
    E --> H[Hardware Info]
    
    F --> I[Data Aggregation]
    G --> I
    H --> I
    
    I --> J[CSV Storage]
    I --> K[KML Generation]
    I --> L[Notification Dispatch]
    
    L --> M[Telegram]
    L --> N[Discord]
    L --> O[Custom Webhook]
```


## 📊 Information Collected

### Device Information
1. Operating System & Platform
2. CPU Cores & Architecture
3. RAM Size
4. GPU Vendor & Renderer
5. Screen Resolution
6. Browser Type & Version

### Network Intelligence
1. Public IP Address

2. ISP (Internet Service Provider)

3. Organization

4. Continent & Country

5. Region & City

### Geolocation Data

1. Latitude & Longitude

2. Accuracy (meters)

3. Altitude

4. Speed (if moving)

5. Direction/Heading

## 🔔 Notification Systems

```mermaid
graph LR
    A[Data Captured] --> B{Notification Type}
    B -->|Telegram| C[Bot API]
    B -->|Discord| D[Webhook API]
    B -->|Custom| E[HTTP POST]
    
    C --> F[Device Info]
    C --> G[Location Data]
    C --> H[IP Info]
    C --> I[Google Maps Link]
    
    D --> F
    D --> G
    D --> H
    D --> I
    
    E --> F
    E --> G
    E --> H
    E --> I
```

## ⚙️ System Requirements

1. Python 3.x

2. PHP 7.0+

3. OS: Linux, Termux, macOS

4. RAM: Minimum 512MB

5. Storage: 100MB free space

6. Network: Internet connection

<div align="center">
🐺 WOLF INTELLIGENCE PK
"Knowledge is Power, Use it Wisely"

Made with ❤️ by ATHEX BLACK HAT

© 2026 WOLF-EYE Framework. All rights reserved.

</div> ```