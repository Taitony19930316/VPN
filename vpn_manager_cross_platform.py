#!/usr/bin/env python3
"""
跨平台VPN管理工具
支持Windows, macOS, Linux
"""

import os
import sys
import json
import yaml
import requests
import subprocess
import platform
import tempfile
import gzip
import shutil
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

class CrossPlatformVPNManager:
    def __init__(self):
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.setup_paths()
        
    def setup_paths(self):
        """设置跨平台路径"""
        if self.system == 'windows':
            self.home_dir = Path.home()
            self.config_dir = self.home_dir / '.config' / 'clash'
            self.clash_binary = 'clash.exe'
            self.mihomo_binary = 'mihomo.exe'
        else:
            self.home_dir = Path.home()
            self.config_dir = self.home_dir / '.config' / 'clash'
            self.clash_binary = 'clash'
            self.mihomo_binary = 'mihomo'
        
        # 创建配置目录
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置配置文件路径
        self.config_file = self.config_dir / 'config.yaml'
        self.pid_file = self.config_dir / 'clash.pid'
        
    def get_download_info(self) -> Tuple[str, str]:
        """获取对应平台的下载信息"""
        # Mihomo (Clash Meta) 下载链接
        base_url = "https://github.com/MetaCubeX/mihomo/releases/latest/download"
        
        if self.system == 'windows':
            if 'amd64' in self.arch or 'x86_64' in self.arch:
                filename = "mihomo-windows-amd64.zip"
            else:
                filename = "mihomo-windows-386.zip"
        elif self.system == 'darwin':  # macOS
            if 'arm64' in self.arch or 'aarch64' in self.arch:
                filename = "mihomo-darwin-arm64.gz"
            else:
                filename = "mihomo-darwin-amd64.gz"
        else:  # Linux
            if 'aarch64' in self.arch or 'arm64' in self.arch:
                filename = "mihomo-linux-arm64.gz"
            elif 'armv7' in self.arch:
                filename = "mihomo-linux-armv7.gz"
            else:
                filename = "mihomo-linux-amd64.gz"
        
        return f"{base_url}/{filename}", filename
    
    def download_mihomo(self) -> bool:
        """下载Mihomo"""
        print("📥 下载Mihomo (Clash Meta)...")
        
        try:
            download_url, filename = self.get_download_info()
            print(f"   下载地址: {download_url}")
            
            # 下载文件
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            temp_file = Path(tempfile.gettempdir()) / filename
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"   ✓ 下载完成: {temp_file}")
            
            # 解压和安装
            return self.install_mihomo(temp_file)
            
        except Exception as e:
            print(f"   ❌ 下载失败: {e}")
            return False
    
    def install_mihomo(self, archive_path: Path) -> bool:
        """安装Mihomo"""
        print("📦 安装Mihomo...")
        
        try:
            # 创建bin目录
            bin_dir = self.home_dir / '.local' / 'bin'
            bin_dir.mkdir(parents=True, exist_ok=True)
            
            target_path = bin_dir / self.mihomo_binary
            
            if archive_path.suffix == '.gz':
                # 处理.gz文件
                with gzip.open(archive_path, 'rb') as f_in:
                    with open(target_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            elif archive_path.suffix == '.zip':
                # 处理.zip文件 (Windows)
                import zipfile
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    # 提取mihomo.exe
                    for file_info in zip_ref.filelist:
                        if file_info.filename.endswith('.exe'):
                            with zip_ref.open(file_info) as source:
                                with open(target_path, 'wb') as target:
                                    shutil.copyfileobj(source, target)
                            break
            
            # 设置执行权限 (非Windows)
            if self.system != 'windows':
                os.chmod(target_path, 0o755)
            
            print(f"   ✓ 安装完成: {target_path}")
            
            # 清理临时文件
            archive_path.unlink()
            
            return True
            
        except Exception as e:
            print(f"   ❌ 安装失败: {e}")
            return False
    
    def find_clash_binary(self) -> Optional[Path]:
        """查找Clash二进制文件"""
        # 可能的路径
        possible_paths = [
            self.home_dir / '.local' / 'bin' / self.mihomo_binary,
            self.home_dir / '.local' / 'bin' / self.clash_binary,
            Path('/usr/local/bin') / self.clash_binary,
            Path('/usr/bin') / self.clash_binary,
        ]
        
        # Windows特殊路径
        if self.system == 'windows':
            possible_paths.extend([
                Path('C:/Program Files/Clash/clash.exe'),
                Path('C:/Program Files (x86)/Clash/clash.exe'),
            ])
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def create_default_config(self):
        """创建默认配置"""
        print("⚙️ 创建默认配置...")
        
        config = {
            'port': 7890,
            'socks-port': 7891,
            'allow-lan': True,
            'mode': 'rule',
            'log-level': 'info',
            'external-controller': '127.0.0.1:9090',
            
            'dns': {
                'enable': True,
                'listen': '0.0.0.0:53',
                'enhanced-mode': 'fake-ip',
                'fake-ip-range': '198.18.0.1/16',
                'nameserver': ['223.5.5.5', '119.29.29.29'],
                'fallback': ['8.8.8.8', '1.1.1.1']
            },
            
            'proxies': [],
            
            'proxy-groups': [
                {
                    'name': '🎯 全球直连',
                    'type': 'select',
                    'proxies': ['DIRECT']
                }
            ],
            
            'rules': [
                'MATCH,🎯 全球直连'
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"   ✓ 配置文件已创建: {self.config_file}")
    
    def start_clash(self) -> bool:
        """启动Clash服务"""
        print("🚀 启动Clash服务...")
        
        # 检查是否已经运行
        if self.is_clash_running():
            print("   ⚠️ Clash已在运行")
            return True
        
        # 查找二进制文件
        clash_binary = self.find_clash_binary()
        if not clash_binary:
            print("   ❌ 未找到Clash二进制文件，尝试下载...")
            if not self.download_mihomo():
                return False
            clash_binary = self.find_clash_binary()
            if not clash_binary:
                print("   ❌ 下载后仍未找到二进制文件")
                return False
        
        # 检查配置文件
        if not self.config_file.exists():
            self.create_default_config()
        
        try:
            # 启动命令
            cmd = [str(clash_binary), '-f', str(self.config_file)]
            
            if self.system == 'windows':
                # Windows下后台启动
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                # Unix系统后台启动
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    preexec_fn=os.setsid
                )
            
            # 保存PID
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            # 等待启动
            import time
            time.sleep(2)
            
            if self.is_clash_running():
                print("   ✅ Clash启动成功")
                self.show_proxy_info()
                return True
            else:
                print("   ❌ Clash启动失败")
                return False
                
        except Exception as e:
            print(f"   ❌ 启动失败: {e}")
            return False
    
    def stop_clash(self) -> bool:
        """停止Clash服务"""
        print("🛑 停止Clash服务...")
        
        try:
            # 通过进程名查找并终止
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and ('clash' in proc.info['name'].lower() or 'mihomo' in proc.info['name'].lower()):
                    proc.terminate()
                    proc.wait(timeout=5)
                    print(f"   ✓ 终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
            
            # 清理PID文件
            if self.pid_file.exists():
                self.pid_file.unlink()
            
            print("   ✅ Clash已停止")
            return True
            
        except Exception as e:
            print(f"   ❌ 停止失败: {e}")
            return False
    
    def is_clash_running(self) -> bool:
        """检查Clash是否运行"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and ('clash' in proc.info['name'].lower() or 'mihomo' in proc.info['name'].lower()):
                    return True
            return False
        except:
            return False
    
    def get_clash_pid(self) -> Optional[int]:
        """获取Clash进程ID"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and ('clash' in proc.info['name'].lower() or 'mihomo' in proc.info['name'].lower()):
                    return proc.info['pid']
            return None
        except:
            return None
    
    def show_status(self):
        """显示服务状态"""
        print("=" * 32)
        print("        VPN服务状态")
        print("=" * 32)
        
        if self.is_clash_running():
            pid = self.get_clash_pid()
            print(f"Clash: 运行中 (PID: {pid})")
            self.show_proxy_info()
        else:
            print("Clash: 未运行")
        
        print("=" * 32)
    
    def show_proxy_info(self):
        """显示代理信息"""
        print("  HTTP代理: 127.0.0.1:7890")
        print("  SOCKS代理: 127.0.0.1:7891")
        print("  控制面板: http://127.0.0.1:9090/ui")
    
    def restart_clash(self) -> bool:
        """重启Clash服务"""
        print("🔄 重启Clash服务...")
        self.stop_clash()
        import time
        time.sleep(1)
        return self.start_clash()
    
    def show_help(self):
        """显示帮助信息"""
        print("VPN管理工具 - 跨平台版本")
        print(f"当前系统: {platform.system()} {platform.machine()}")
        print()
        print("使用方法:")
        print("  python vpn_manager_cross_platform.py <命令>")
        print()
        print("可用命令:")
        print("  start    - 启动VPN服务")
        print("  stop     - 停止VPN服务")
        print("  restart  - 重启VPN服务")
        print("  status   - 查看服务状态")
        print("  install  - 安装Mihomo")
        print("  help     - 显示此帮助信息")
        print()
        print("代理设置:")
        print("  HTTP代理: 127.0.0.1:7890")
        print("  SOCKS代理: 127.0.0.1:7891")
        print("  控制面板: http://127.0.0.1:9090/ui")

def main():
    """主函数"""
    manager = CrossPlatformVPNManager()
    
    if len(sys.argv) < 2:
        manager.show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        manager.start_clash()
    elif command == 'stop':
        manager.stop_clash()
    elif command == 'restart':
        manager.restart_clash()
    elif command == 'status':
        manager.show_status()
    elif command == 'install':
        manager.download_mihomo()
    elif command == 'help':
        manager.show_help()
    else:
        print(f"❌ 未知命令: {command}")
        manager.show_help()

if __name__ == "__main__":
    main()