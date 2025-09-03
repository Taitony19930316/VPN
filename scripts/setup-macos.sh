#!/bin/bash

echo "================================"
echo "   智能分流VPN配置 - macOS"
echo "================================"
echo

# 检查是否安装了Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew未安装，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "[1/5] 安装Clash..."
if ! command -v clash &> /dev/null; then
    brew install clash
fi

echo "[2/5] 创建配置目录..."
mkdir -p ~/.config/clash

echo "[3/5] 复制配置文件..."
cp config/clash-config.yaml ~/.config/clash/config.yaml

echo "[4/5] 设置权限..."
chmod 644 ~/.config/clash/config.yaml

echo "[5/5] 启动Clash..."
echo "正在后台启动Clash..."
nohup clash -d ~/.config/clash > /dev/null 2>&1 &

echo
echo "================================"
echo "配置完成！使用说明："
echo "1. Clash已在后台运行"
echo "2. HTTP代理: 127.0.0.1:7890"
echo "3. SOCKS代理: 127.0.0.1:7891"
echo "4. 控制面板: http://127.0.0.1:9090/ui"
echo "================================"
echo
echo "设置系统代理："
echo "系统偏好设置 → 网络 → 高级 → 代理"
echo "HTTP代理: 127.0.0.1:7890"
echo "HTTPS代理: 127.0.0.1:7890"
echo
echo "测试命令："
echo "  curl -I https://github.com"
echo "  curl -I https://baidu.com"
echo