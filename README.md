# VPN智能分流系统

🚀 一个完整的跨平台VPN智能分流解决方案，专为开发者设计

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/your-username/vpn-smart-routing)

[English](README_EN.md) | 中文

## ✨ 特性

- 🎯 **智能分流**: 自动识别国内外网站，智能选择直连或代理
- 🛠️ **开发友好**: 针对GitHub、npm、pip等开发工具优化
- 🖥️ **简单易用**: 一键启动，图形化管理界面
- 🔧 **多协议支持**: 支持Shadowsocks、VMess、Trojan等
- 📊 **实时监控**: 内置测试工具和性能监控
- 🔒 **安全可靠**: 使用最新加密协议，定期更新维护

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip3 install -r requirements.txt

# macOS用户安装Clash
brew install clash
```

### 2. 启动系统

```bash
# 方式1: 使用图形界面 (推荐)
python3 vpn_launcher.py

# 方式2: 命令行启动
python3 vpn_manager.py start
```

### 3. 配置代理

启动后在浏览器或应用中设置代理:
- HTTP代理: `127.0.0.1:7890`
- SOCKS代理: `127.0.0.1:7891`

## 📋 主要命令

```bash
# 服务管理
python3 vpn_manager.py start      # 启动VPN服务
python3 vpn_manager.py stop       # 停止VPN服务
python3 vpn_manager.py status     # 查看运行状态

# 测试工具
python3 complete_test.py          # 完整系统测试
python3 test_vpn_connectivity.py # 连接测试
python3 test_vpn_speed.py        # 速度测试

# 配置工具
python3 create_simple_config.py  # 创建基础配置
python3 config_validator.py      # 验证配置文件
```

## 🌐 智能分流规则

### 自动代理访问
- 🔧 **开发工具**: GitHub, GitLab, npm, PyPI, Docker Hub
- 🔍 **搜索引擎**: Google, Bing, DuckDuckGo  
- 📺 **视频网站**: YouTube, Vimeo, Twitch
- 💬 **社交媒体**: Twitter, Facebook, Instagram
- 📚 **知识网站**: Wikipedia, Stack Overflow, Medium

### 直连访问
- 🏪 **电商平台**: 淘宝, 京东, 拼多多
- 📺 **视频网站**: 爱奇艺, 优酷, 哔哩哔哩
- 🔍 **搜索引擎**: 百度, 搜狗, 360搜索
- 🏦 **金融服务**: 支付宝, 微信, 银行网站
- 📱 **国内服务**: 腾讯, 阿里巴巴, 新浪

## 📁 项目结构

```
vpn-project/
├── vpn_launcher.py          # 🚀 主启动器
├── vpn_manager.py           # 🛠️ VPN管理工具  
├── complete_test.py         # 🧪 完整测试工具
├── config/                  # ⚙️ 配置文件
├── scripts/                 # 📜 辅助脚本
├── docs/                    # 📖 文档目录
├── logs/                    # 📋 日志文件
└── requirements.txt         # 📦 依赖列表
```

## 🔧 故障排除

### 常见问题

1. **无法启动服务**
   ```bash
   # 检查Clash是否安装
   clash -v
   
   # 验证配置文件
   python3 config_validator.py
   ```

2. **网络连接失败**
   ```bash
   # 运行连接测试
   python3 test_vpn_connectivity.py
   
   # 检查代理设置
   curl -x http://127.0.0.1:7890 http://httpbin.org/ip
   ```

3. **速度较慢**
   ```bash
   # 运行速度测试
   python3 test_vpn_speed.py
   
   # 尝试不同配置
   python3 vpn_manager.py config
   ```

### 获取帮助

```bash
# 查看详细帮助
python3 vpn_manager.py help

# 运行系统诊断
python3 complete_test.py

# 查看日志文件
tail -f logs/clash.log
```

## 🎯 使用场景

- 👨‍💻 **开发工作**: 访问GitHub、Stack Overflow等开发资源
- 📚 **学习研究**: 查阅国外技术文档和论文
- 🛍️ **日常使用**: 购物、娱乐等日常网络活动
- 🏢 **企业环境**: 团队协作和项目管理

## 🔒 安全说明

- 使用最新的加密协议确保数据安全
- 定期更新软件版本修复安全漏洞  
- 建议使用强密码和定期更换配置
- 遵守当地法律法规，合理使用网络资源

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目！

---

⭐ 如果这个项目对你有帮助，请给个星标支持一下！
