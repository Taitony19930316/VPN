#!/usr/bin/env python3
"""
VPN项目主启动器
一键启动和管理整个VPN系统
"""

import sys
import subprocess
from pathlib import Path

def show_menu():
    """显示主菜单"""
    print("=" * 50)
    print("        VPN智能分流系统")
    print("=" * 50)
    print("1. 🚀 启动VPN服务")
    print("2. 🛑 停止VPN服务") 
    print("3. 🔄 重启VPN服务")
    print("4. 📊 查看服务状态")
    print("5. 🧪 运行完整测试")
    print("6. ⚙️  配置管理")
    print("7. 📝 查看日志")
    print("8. ❓ 帮助信息")
    print("9. 🚪 退出")
    print("=" * 50)

def run_command(cmd):
    """运行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"命令执行失败: {e}")
        return False

def main():
    """主函数"""
    while True:
        show_menu()
        choice = input("请选择操作 (1-9): ").strip()
        
        if choice == '1':
            print("🚀 启动VPN服务...")
            run_command("python3 vpn_manager.py start")
            
        elif choice == '2':
            print("🛑 停止VPN服务...")
            run_command("python3 vpn_manager.py stop")
            
        elif choice == '3':
            print("🔄 重启VPN服务...")
            run_command("python3 vpn_manager.py restart")
            
        elif choice == '4':
            print("📊 查看服务状态...")
            run_command("python3 vpn_manager.py status")
            
        elif choice == '5':
            print("🧪 运行完整测试...")
            run_command("python3 complete_test.py")
            
        elif choice == '6':
            print("⚙️ 配置管理...")
            print("可用配置文件:")
            config_dir = Path("config")
            if config_dir.exists():
                for config_file in config_dir.glob("*.yaml"):
                    print(f"  - {config_file.name}")
            print("使用 python3 vpn_manager.py config 管理配置")
            
        elif choice == '7':
            print("📝 查看日志...")
            log_files = ["logs/clash.log", "logs/vpn_manager.log"]
            for log_file in log_files:
                if Path(log_file).exists():
                    print(f"\n--- {log_file} ---")
                    run_command(f"tail -20 {log_file}")
                    
        elif choice == '8':
            print("❓ 帮助信息...")
            run_command("python3 vpn_manager.py help")
            
        elif choice == '9':
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择，请重试")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
