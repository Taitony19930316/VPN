# VPN智能分流系统 - 跨平台版

🚀 支持Windows、macOS、Linux的VPN智能分流解决方案

## ✨ 特性

- 🌍 **跨平台支持**: Windows, macOS, Linux
- 🎯 **智能分流**: 自动识别国内外网站
- 🛠️ **开发友好**: 针对开发工具优化
- 📦 **一键安装**: 自动下载和配置
- 🖥️ **图形界面**: 简单易用的管理界面
- 🔧 **命令行工具**: 支持脚本自动化

## 🚀 快速开始

### Windows用户

1. **下载项目文件**
2. **运行安装脚本**
   ```cmd
   install.bat
   ```
3. **启动VPN**
   ```cmd
   # 方式1: 图形界面
   start_vpn.bat
   
   # 方式2: 命令行
   vpn.bat start
   ```

### macOS/Linux用户

1. **下载项目文件**
2. **运行安装脚本**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
3. **启动VPN**
   ```bash
   # 方式1: 图形界面
   python3 vpn_launcher_cross_platform.py
   
   # 方式2: 命令行
   python3 vpn_manager_cross_platform.py start
   ```

## 📋 核心文件

```
vpn-project/
├── vpn_manager_cross_platform.py    # 跨平台VPN管理工具
├── vpn_launcher_cross_platform.py   # 跨平台图形启动器
├── install.bat                      # Windows安装脚本
├── install.sh                       # Unix安装脚本
├── requirements.txt                 # Python依赖
├── config/                          # 配置文件目录
└── README_CROSS_PLATFORM.md        # 本文档
```

## 🎮 使用方法

### 图形界面

启动图形界面后，你可以通过菜单进行操作：

1. 🚀 启动VPN服务
2. 🛑 停止VPN服务
3. 🔄 重启VPN服务
4. 📊 查看服务状态
5. 📦 安装/更新Mihomo
6. 🧪 运行网络测试
7. ⚙️ 配置管理
8. 📝 查看日志
9. ❓ 帮助信息

### 命令行工具

```bash
# Windows
vpn.bat <命令>

# macOS/Linux
python3 vpn_manager_cross_platform.py <命令>
```

可用命令：
- `start` - 启动VPN服务
- `stop` - 停止VPN服务
- `restart` - 重启VPN服务
- `status` - 查看服务状态
- `install` - 安装Mihomo
- `help` - 显示帮助信息

## 🌐 代理设置

启动服务后，在应用程序中设置以下代理：

- **HTTP代理**: `127.0.0.1:7890`
- **SOCKS代理**: `127.0.0.1:7891`
- **控制面板**: `http://127.0.0.1:9090/ui`

## ⚙️ 配置文件

配置文件位置：
- **Windows**: `%USERPROFILE%\.config\clash\config.yaml`
- **macOS/Linux**: `~/.config/clash/config.yaml`

### 添加代理服务器

编辑配置文件，在 `proxies` 部分添加你的代理服务器：

```yaml
proxies:
  - name: "我的代理"
    type: ss
    server: your-server.com
    port: 443
    cipher: aes-256-gcm
    password: your-password

proxy-groups:
  - name: "🚀 代理选择"
    type: select
    proxies:
      - "我的代理"
      - "DIRECT"

rules:
  - DOMAIN-SUFFIX,google.com,🚀 代理选择
  - DOMAIN-SUFFIX,github.com,🚀 代理选择
  - GEOIP,CN,DIRECT
  - MATCH,🚀 代理选择
```

## 🔧 故障排除

### 1. 服务无法启动

```bash
# 检查是否已安装依赖
pip install -r requirements.txt

# 手动安装Mihomo
python3 vpn_manager_cross_platform.py install
```

### 2. 网络连接问题

```bash
# 运行网络测试
# 在图形界面选择"运行网络测试"

# 或手动测试
curl -x http://127.0.0.1:7890 http://httpbin.org/ip
```

### 3. 配置文件问题

- 检查配置文件语法是否正确
- 确保代理服务器信息准确
- 重启服务使配置生效

### 4. 权限问题 (macOS/Linux)

```bash
# 设置执行权限
chmod +x vpn_manager_cross_platform.py
chmod +x vpn_launcher_cross_platform.py
```

## 🎯 智能分流规则

系统会自动识别并分流：

### 代理访问
- 🔧 开发工具: GitHub, GitLab, npm, PyPI
- 🔍 搜索引擎: Google, Bing
- 📺 视频网站: YouTube, Vimeo
- 💬 社交媒体: Twitter, Facebook
- 📚 知识网站: Wikipedia, Stack Overflow

### 直连访问
- 🏪 电商平台: 淘宝, 京东, 拼多多
- 📺 视频网站: 爱奇艺, 优酷, 哔哩哔哩
- 🔍 搜索引擎: 百度, 搜狗, 360
- 🏦 金融服务: 支付宝, 微信
- 📱 国内服务: 腾讯, 阿里巴巴

## 📱 系统要求

- **Python**: 3.7+
- **操作系统**: Windows 10+, macOS 10.14+, Linux (主流发行版)
- **网络**: 互联网连接
- **内存**: 至少100MB可用内存

## 🔒 安全说明

- 使用最新的Mihomo (Clash Meta)内核
- 支持现代加密协议
- 定期更新确保安全性
- 遵守当地法律法规

## 📄 许可证

本项目采用 MIT 许可证

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

⭐ 如果这个项目对你有帮助，请给个星标支持！