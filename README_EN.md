# VPN Smart Routing System

🚀 A complete cross-platform VPN smart routing solution designed for developers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/your-username/vpn-smart-routing)

English | [中文](README.md)

## ✨ Features

- 🌍 **Cross-Platform**: Windows, macOS, Linux support
- 🎯 **Smart Routing**: Automatically route domestic/international traffic
- 🛠️ **Developer Friendly**: Optimized for GitHub, npm, pip, etc.
- 📦 **One-Click Install**: Automatic download and configuration
- 🖥️ **GUI Interface**: User-friendly management interface
- 🔧 **CLI Tools**: Support for script automation

## 🚀 Quick Start

### Windows Users

1. **Download project files**
2. **Run installation script**
   ```cmd
   install.bat
   ```
3. **Start VPN**
   ```cmd
   # GUI mode
   start_vpn.bat
   
   # Command line
   vpn.bat start
   ```

### macOS/Linux Users

1. **Download project files**
2. **Run installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
3. **Start VPN**
   ```bash
   # GUI mode
   python3 vpn_launcher_cross_platform.py
   
   # Command line
   python3 vpn_manager_cross_platform.py start
   ```

## 📋 Core Files

```
vpn-project/
├── vpn_manager_cross_platform.py    # Cross-platform VPN manager
├── vpn_launcher_cross_platform.py   # Cross-platform GUI launcher
├── install.bat                      # Windows installer
├── install.sh                       # Unix installer
├── requirements.txt                 # Python dependencies
├── config/                          # Configuration files
└── README_CROSS_PLATFORM.md        # Detailed documentation
```

## 🌐 Proxy Settings

After starting the service, configure the following proxy settings:

- **HTTP Proxy**: `127.0.0.1:7890`
- **SOCKS Proxy**: `127.0.0.1:7891`
- **Control Panel**: `http://127.0.0.1:9090/ui`

## 🎯 Smart Routing Rules

### Proxied Services
- 🔧 **Dev Tools**: GitHub, GitLab, npm, PyPI, Docker Hub
- 🔍 **Search**: Google, Bing, DuckDuckGo
- 📺 **Video**: YouTube, Vimeo, Twitch
- 💬 **Social**: Twitter, Facebook, Instagram
- 📚 **Knowledge**: Wikipedia, Stack Overflow, Medium

### Direct Access
- 🏪 **E-commerce**: Taobao, JD, PDD
- 📺 **Video**: iQiyi, Youku, Bilibili
- 🔍 **Search**: Baidu, Sogou, 360
- 🏦 **Finance**: Alipay, WeChat Pay
- 📱 **Services**: Tencent, Alibaba, Sina

## 🔧 Troubleshooting

### 1. Service Won't Start

```bash
# Check dependencies
pip install -r requirements.txt

# Manual install Mihomo
python3 vpn_manager_cross_platform.py install
```

### 2. Network Issues

```bash
# Test network
curl -x http://127.0.0.1:7890 http://httpbin.org/ip
```

### 3. Permission Issues (macOS/Linux)

```bash
# Set permissions
chmod +x vpn_manager_cross_platform.py
chmod +x vpn_launcher_cross_platform.py
```

## 📱 System Requirements

- **Python**: 3.7+
- **OS**: Windows 10+, macOS 10.14+, Linux (mainstream distributions)
- **Network**: Internet connection
- **Memory**: At least 100MB available memory

## 🔒 Security

- Uses latest Mihomo (Clash Meta) kernel
- Supports modern encryption protocols
- Regular updates for security
- Complies with local laws and regulations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

⭐ If this project helps you, please give it a star!