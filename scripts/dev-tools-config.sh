#!/bin/bash

echo "================================"
echo "   开发工具代理配置脚本"
echo "================================"
echo

PROXY_HTTP="http://127.0.0.1:7890"
PROXY_SOCKS="socks5://127.0.0.1:7891"

echo "[1/6] 配置Git代理..."
git config --global http.proxy $PROXY_HTTP
git config --global https.proxy $PROXY_HTTP
# 只对GitHub使用代理
git config --global http.https://github.com.proxy $PROXY_HTTP
echo "✅ Git代理配置完成"

echo "[2/6] 配置npm代理..."
npm config set proxy $PROXY_HTTP
npm config set https-proxy $PROXY_HTTP
npm config set registry https://registry.npmjs.org/
echo "✅ npm代理配置完成"

echo "[3/6] 配置yarn代理..."
if command -v yarn &> /dev/null; then
    yarn config set proxy $PROXY_HTTP
    yarn config set https-proxy $PROXY_HTTP
    echo "✅ yarn代理配置完成"
else
    echo "⚠️  yarn未安装，跳过配置"
fi

echo "[4/6] 配置pip代理..."
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
proxy = $PROXY_HTTP
trusted-host = pypi.org
               pypi.python.org
               files.pythonhosted.org
EOF
echo "✅ pip代理配置完成"

echo "[5/6] 配置Docker代理..."
mkdir -p ~/.docker
cat > ~/.docker/config.json << EOF
{
    "proxies": {
        "default": {
            "httpProxy": "$PROXY_HTTP",
            "httpsProxy": "$PROXY_HTTP"
        }
    }
}
EOF
echo "✅ Docker代理配置完成"

echo "[6/6] 配置环境变量..."
cat >> ~/.bashrc << EOF

# VPN代理环境变量
export http_proxy=$PROXY_HTTP
export https_proxy=$PROXY_HTTP
export HTTP_PROXY=$PROXY_HTTP
export HTTPS_PROXY=$PROXY_HTTP

# 代理管理函数
proxy_on() {
    export http_proxy=$PROXY_HTTP
    export https_proxy=$PROXY_HTTP
    export HTTP_PROXY=$PROXY_HTTP
    export HTTPS_PROXY=$PROXY_HTTP
    echo "✅ 代理已开启"
}

proxy_off() {
    unset http_proxy
    unset https_proxy
    unset HTTP_PROXY
    unset HTTPS_PROXY
    echo "✅ 代理已关闭"
}

proxy_status() {
    if [ -n "\$http_proxy" ]; then
        echo "🟢 代理状态: 开启 (\$http_proxy)"
    else
        echo "🔴 代理状态: 关闭"
    fi
}
EOF

echo "✅ 环境变量配置完成"

echo
echo "================================"
echo "开发工具代理配置完成！"
echo "================================"
echo
echo "使用方法："
echo "• proxy_on    - 开启终端代理"
echo "• proxy_off   - 关闭终端代理"  
echo "• proxy_status - 查看代理状态"
echo
echo "重新加载配置："
echo "  source ~/.bashrc"
echo
echo "测试代理："
echo "  curl -I https://github.com"
echo "  npm info react"
echo "  pip search requests"
echo