#!/usr/bin/env python3
"""
跨平台VPN启动器
支持Windows, macOS, Linux的图形化管理界面
"""

import sys
import subprocess
import platform
from pathlib import Path

class CrossPlatformLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.manager_script = 'vpn_manager_cross_platform.py'
        
    def show_menu(self):
        """显示主菜单"""
        print("=" * 50)
        print("        VPN智能分流系统")
        print(f"        {platform.system()} {platform.machine()}")
        print("=" * 50)
        print("1. 🚀 启动VPN服务")
        print("2. 🛑 停止VPN服务") 
        print("3. 🔄 重启VPN服务")
        print("4. 📊 查看服务状态")
        print("5. 📦 安装/更新Mihomo")
        print("6. 🧪 运行网络测试")
        print("7. ⚙️  配置管理")
        print("8. 📝 查看日志")
        print("9. ❓ 帮助信息")
        print("0. 🚪 退出")
        print("=" * 50)

    def run_command(self, cmd):
        """运行命令"""
        try:
            if isinstance(cmd, str):
                cmd = cmd.split()
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            return result.returncode == 0
        except Exception as e:
            print(f"命令执行失败: {e}")
            return False

    def test_network(self):
        """简单的网络测试"""
        print("🧪 运行网络测试...")
        
        import requests
        
        # 测试直连
        try:
            response = requests.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ 直连测试成功，IP: {ip_info.get('origin', 'Unknown')}")
            else:
                print(f"❌ 直连测试失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ 直连测试失败: {e}")
        
        # 测试代理连接
        try:
            proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ 代理测试成功，IP: {ip_info.get('origin', 'Unknown')}")
            else:
                print(f"❌ 代理测试失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ 代理测试失败: {e}")

    def show_config_info(self):
        """显示配置信息"""
        print("⚙️ 配置管理...")
        
        if self.system == 'windows':
            config_dir = Path.home() / '.config' / 'clash'
        else:
            config_dir = Path.home() / '.config' / 'clash'
        
        print(f"配置目录: {config_dir}")
        
        if config_dir.exists():
            print("可用配置文件:")
            for config_file in config_dir.glob("*.yaml"):
                print(f"  - {config_file.name}")
            for config_file in config_dir.glob("*.yml"):
                print(f"  - {config_file.name}")
        else:
            print("配置目录不存在")
        
        print("\n💡 配置文件说明:")
        print("  - config.yaml: 主配置文件")
        print("  - 可以手动编辑配置文件添加代理服务器")
        print("  - 重启服务后配置生效")

    def show_logs(self):
        """显示日志"""
        print("📝 查看日志...")
        
        log_files = []
        
        # 查找可能的日志文件位置
        possible_log_dirs = [
            Path.cwd() / 'logs',
            Path.home() / '.config' / 'clash',
            Path('/tmp') if self.system != 'windows' else Path.home() / 'AppData' / 'Local' / 'Temp'
        ]
        
        for log_dir in possible_log_dirs:
            if log_dir.exists():
                for log_file in log_dir.glob("*.log"):
                    log_files.append(log_file)
        
        if log_files:
            for log_file in log_files:
                print(f"\n--- {log_file} ---")
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # 显示最后20行
                        for line in lines[-20:]:
                            print(line.rstrip())
                except Exception as e:
                    print(f"读取日志失败: {e}")
        else:
            print("未找到日志文件")

    def wait_for_input(self):
        """等待用户输入"""
        if self.system == 'windows':
            input("\n按回车键继续...")
        else:
            input("\n按回车键继续...")

    def main_loop(self):
        """主循环"""
        while True:
            try:
                self.show_menu()
                choice = input("请选择操作 (0-9): ").strip()
                
                if choice == '1':
                    print("🚀 启动VPN服务...")
                    self.run_command(['python', self.manager_script, 'start'])
                    
                elif choice == '2':
                    print("🛑 停止VPN服务...")
                    self.run_command(['python', self.manager_script, 'stop'])
                    
                elif choice == '3':
                    print("🔄 重启VPN服务...")
                    self.run_command(['python', self.manager_script, 'restart'])
                    
                elif choice == '4':
                    print("📊 查看服务状态...")
                    self.run_command(['python', self.manager_script, 'status'])
                    
                elif choice == '5':
                    print("📦 安装/更新Mihomo...")
                    self.run_command(['python', self.manager_script, 'install'])
                    
                elif choice == '6':
                    self.test_network()
                    
                elif choice == '7':
                    self.show_config_info()
                    
                elif choice == '8':
                    self.show_logs()
                    
                elif choice == '9':
                    print("❓ 帮助信息...")
                    self.run_command(['python', self.manager_script, 'help'])
                    
                elif choice == '0':
                    print("👋 再见！")
                    break
                    
                else:
                    print("❌ 无效选择，请重试")
                
                self.wait_for_input()
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"发生错误: {e}")
                self.wait_for_input()

def main():
    """主函数"""
    print("🚀 VPN智能分流系统启动中...")
    
    launcher = CrossPlatformLauncher()
    launcher.main_loop()

if __name__ == "__main__":
    main()