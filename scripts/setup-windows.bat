@echo off
chcp 65001 >nul
echo ================================
echo    智能分流VPN配置 - Windows
echo ================================
echo.

echo [1/4] 检查Clash是否已安装...
where clash >nul 2>&1
if %errorlevel% neq 0 (
    echo Clash未找到，请先下载并安装Clash for Windows
    echo 下载地址: https://github.com/Fndroid/clash_for_windows_pkg/releases
    pause
    exit /b 1
)

echo [2/4] 创建配置目录...
if not exist "%USERPROFILE%\.config\clash" mkdir "%USERPROFILE%\.config\clash"

echo [3/4] 复制配置文件...
copy "config\clash-config.yaml" "%USERPROFILE%\.config\clash\config.yaml"

echo [4/4] 设置系统代理...
echo 请手动在Clash中启用系统代理，端口设置为7890

echo.
echo ================================
echo 配置完成！使用说明：
echo 1. 启动Clash for Windows
echo 2. 导入配置文件或直接使用已复制的配置
echo 3. 开启系统代理
echo 4. 选择"自动选择"模式
echo ================================
echo.
echo 测试命令：
echo   curl -I https://github.com
echo   curl -I https://baidu.com
echo.
pause