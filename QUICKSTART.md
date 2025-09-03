# VPN智能分流系统 - 快速开始

## 🚀 一键启动

```bash
# 启动主界面
python3 vpn_launcher.py

# 或者直接使用命令行
python3 vpn_manager.py start
```

## 📋 基本命令

```bash
# 服务管理
python3 vpn_manager.py start      # 启动服务
python3 vpn_manager.py stop       # 停止服务  
python3 vpn_manager.py restart    # 重启服务
python3 vpn_manager.py status     # 查看状态

# 测试和验证
python3 complete_test.py          # 完整系统测试
python3 test_vpn_connectivity.py # 连接性测试
python3 test_vpn_speed.py        # 速度测试

# 配置管理
python3 create_simple_config.py  # 创建简单配置
python3 config_validator.py      # 验证配置文件
```

## 🌐 代理设置

启动后可使用以下代理设置:

- **HTTP代理**: `127.0.0.1:7890`
- **SOCKS代理**: `127.0.0.1:7891` 
- **控制面板**: `http://127.0.0.1:9090/ui`

## 📁 项目结构

```
vpn-project/
├── vpn_launcher.py          # 主启动器 (推荐使用)
├── vpn_manager.py           # VPN管理工具
├── complete_test.py         # 完整测试工具
├── config/                  # 配置文件目录
│   ├── working-config.yaml  # 工作配置
│   └── test-config.yaml     # 测试配置
├── scripts/                 # 脚本文件
├── docs/                    # 文档目录
└── logs/                    # 日志文件
```

## 🔧 故障排除

1. **服务无法启动**
   ```bash
   # 检查配置文件
   python3 config_validator.py
   
   # 查看详细日志
   tail -f logs/clash.log
   ```

2. **网络连接问题**
   ```bash
   # 运行网络测试
   python3 test_vpn_connectivity.py
   
   # 检查代理设置
   curl -x http://127.0.0.1:7890 http://httpbin.org/ip
   ```

3. **配置文件问题**
   ```bash
   # 创建新的简单配置
   python3 create_simple_config.py
   
   # 验证配置语法
   python3 config_validator.py config/working-config.yaml
   ```

## 💡 使用建议

1. **首次使用**: 运行 `python3 vpn_launcher.py` 使用图形界面
2. **日常使用**: 使用 `python3 vpn_manager.py start/stop` 命令
3. **问题诊断**: 运行 `python3 complete_test.py` 进行全面检查
4. **性能测试**: 使用 `python3 test_vpn_speed.py` 测试速度

## 🎯 智能分流

系统会自动识别并分流:
- **国外网站** (GitHub, Google等) → 代理访问
- **国内网站** (百度, 淘宝等) → 直连访问
- **开发工具** (npm, pip等) → 智能选择

---

🎉 享受智能分流带来的便利！
