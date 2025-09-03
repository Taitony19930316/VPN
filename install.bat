@echo off
REM Windows安装脚本
echo ========================================
echo        VPN智能分流系统 - Windows安装
echo ========================================

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

REM 安装依赖
echo 📦 安装Python依赖...
pip install requests pyyaml psutil

if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ✅ 依赖安装完成

REM 创建配置目录
echo 📁 创建配置目录...
if not exist "%USERPROFILE%\.config\clash" (
    mkdir "%USERPROFILE%\.config\clash"
)

echo ✅ 配置目录已创建

REM 创建启动脚本
echo 🚀 创建启动脚本...
echo @echo off > start_vpn.bat
echo python vpn_launcher_cross_platform.py >> start_vpn.bat

echo @echo off > vpn.bat
echo python vpn_manager_cross_platform.py %%* >> vpn.bat

echo ✅ 启动脚本已创建

echo.
echo ========================================
echo           安装完成！
echo ========================================
echo.
echo 💡 使用方法:
echo   1. 双击 start_vpn.bat 启动图形界面
echo   2. 或在命令行运行: vpn.bat start
echo.
echo 📋 可用命令:
echo   vpn.bat start    - 启动VPN服务
echo   vpn.bat stop     - 停止VPN服务
echo   vpn.bat status   - 查看状态
echo   vpn.bat help     - 显示帮助
echo.
echo 🌐 代理设置:
echo   HTTP代理: 127.0.0.1:7890
echo   SOCKS代理: 127.0.0.1:7891
echo.
pause