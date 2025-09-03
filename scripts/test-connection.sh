#!/bin/bash

echo "================================"
echo "    VPN连接测试脚本"
echo "================================"
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
test_connection() {
    local url=$1
    local name=$2
    local expected=$3
    
    echo -n "测试 $name ... "
    
    if curl -s --connect-timeout 5 --max-time 10 -I "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 成功${NC}"
        return 0
    else
        echo -e "${RED}❌ 失败${NC}"
        return 1
    fi
}

# 检查代理状态
echo "🔍 检查代理状态..."
if [ -n "$http_proxy" ]; then
    echo -e "代理状态: ${GREEN}开启${NC} ($http_proxy)"
else
    echo -e "代理状态: ${YELLOW}关闭${NC}"
fi
echo

# 测试基础连接
echo "🌐 测试基础网络连接..."
test_connection "https://baidu.com" "百度 (国内直连)" "direct"
test_connection "https://github.com" "GitHub (代理)" "proxy"
test_connection "https://google.com" "Google (代理)" "proxy"
echo

# 测试开发工具
echo "🛠️  测试开发工具连接..."
test_connection "https://registry.npmjs.org" "npm registry" "proxy"
test_connection "https://pypi.org" "PyPI" "proxy"
test_connection "https://hub.docker.com" "Docker Hub" "proxy"
test_connection "https://golang.org" "Go官网" "proxy"
echo

# 测试国内服务
echo "🏠 测试国内服务连接..."
test_connection "https://gitee.com" "Gitee" "direct"
test_connection "https://registry.npmmirror.com" "npm淘宝镜像" "direct"
test_connection "https://bilibili.com" "哔哩哔哩" "direct"
test_connection "https://zhihu.com" "知乎" "direct"
echo

# 获取IP信息
echo "🌍 获取IP信息..."
echo -n "当前IP: "
current_ip=$(curl -s --connect-timeout 5 ipinfo.io/ip 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}$current_ip${NC}"
    
    # 获取IP详细信息
    ip_info=$(curl -s --connect-timeout 5 ipinfo.io 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "IP详情:"
        echo "$ip_info" | jq . 2>/dev/null || echo "$ip_info"
    fi
else
    echo -e "${RED}获取失败${NC}"
fi
echo

# DNS测试
echo "🔍 DNS解析测试..."
echo -n "GitHub DNS: "
github_ip=$(nslookup github.com 2>/dev/null | grep "Address:" | tail -1 | awk '{print $2}')
if [ -n "$github_ip" ]; then
    echo -e "${GREEN}$github_ip${NC}"
else
    echo -e "${RED}解析失败${NC}"
fi

echo -n "百度 DNS: "
baidu_ip=$(nslookup baidu.com 2>/dev/null | grep "Address:" | tail -1 | awk '{print $2}')
if [ -n "$baidu_ip" ]; then
    echo -e "${GREEN}$baidu_ip${NC}"
else
    echo -e "${RED}解析失败${NC}"
fi
echo

# 速度测试
echo "⚡ 简单速度测试..."
echo -n "GitHub下载速度: "
github_speed=$(curl -s -w "%{speed_download}" -o /dev/null --connect-timeout 10 --max-time 30 "https://github.com/microsoft/vscode/archive/refs/heads/main.zip" 2>/dev/null)
if [ $? -eq 0 ] && [ "$github_speed" != "0.000" ]; then
    speed_mb=$(echo "scale=2; $github_speed / 1024 / 1024" | bc 2>/dev/null || echo "N/A")
    echo -e "${GREEN}${speed_mb} MB/s${NC}"
else
    echo -e "${YELLOW}测试超时或失败${NC}"
fi

echo -n "百度下载速度: "
baidu_speed=$(curl -s -w "%{speed_download}" -o /dev/null --connect-timeout 10 --max-time 30 "https://www.baidu.com" 2>/dev/null)
if [ $? -eq 0 ] && [ "$baidu_speed" != "0.000" ]; then
    speed_kb=$(echo "scale=2; $baidu_speed / 1024" | bc 2>/dev/null || echo "N/A")
    echo -e "${GREEN}${speed_kb} KB/s${NC}"
else
    echo -e "${YELLOW}测试超时或失败${NC}"
fi
echo

# 总结
echo "================================"
echo "测试完成！"
echo "================================"
echo
echo "💡 使用建议："
echo "• 如果GitHub访问失败，检查代理服务器设置"
echo "• 如果国内网站变慢，检查分流规则配置"
echo "• 定期运行此脚本检查连接状态"
echo "• 遇到问题可查看客户端日志"
echo