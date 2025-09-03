#!/bin/bash
# macOS/Linux安装脚本

echo "========================================"
echo "    VPN智能分流系统 - Unix安装"
echo "========================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

echo "✅ Python3已安装"

# 安装依赖
echo "📦 安装Python依赖..."
pip3 install requests pyyaml psutil

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装完成"

# 创建配置目录
echo "📁 创建配置目录..."
mkdir -p ~/.config/clash

echo "✅ 配置目录已创建"

# 设置执行权限
echo "🔐 设置执行权限..."
chmod +x vpn_manager_cross_platform.py
chmod +x vpn_launcher_cross_platform.py
chmod +x install.sh

# 创建符号链接（可选）
if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    echo "🔗 创建系统链接..."
    ln -sf "$(pwd)/vpn_manager_cross_platform.py" /usr/local/bin/vpn
    echo "   ✓ 可以使用 'vpn' 命令"
fi

echo "✅ 权限设置完成"

echo ""
echo "========================================"
echo "           安装完成！"
echo "========================================"
echo ""
echo "💡 使用方法:"
echo "  1. 运行: python3 vpn_launcher_cross_platform.py"
echo "  2. 或命令行: python3 vpn_manager_cross_platform.py start"
echo ""
echo "📋 可用命令:"
echo "  python3 vpn_manager_cross_platform.py start    - 启动VPN服务"
echo "  python3 vpn_manager_cross_platform.py stop     - 停止VPN服务"
echo "  python3 vpn_manager_cross_platform.py status   - 查看状态"
echo "  python3 vpn_manager_cross_platform.py help     - 显示帮助"
echo ""
echo "🌐 代理设置:"
echo "  HTTP代理: 127.0.0.1:7890"
echo "  SOCKS代理: 127.0.0.1:7891"
echo ""