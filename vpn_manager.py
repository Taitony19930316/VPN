#!/usr/bin/env python3
"""
VPN管理工具 - Python版本
支持Clash/Mihomo的安装、配置和管理
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
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

class Colors:
    """终端颜色输出"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class Logger:
    """日志输出工具"""
    
    @staticmethod
    def info(message: str):
        print(f"{Colors.GREEN}[INFO]{Colors.NC} {message}")
    
    @staticmethod
    def warn(message: str):
        print(f"{Colors.YELLOW}[WARN]{Colors.NC} {message}")
    
    @staticmethod
    def error(message: str):
        print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")
    
    @staticmethod
    def debug(message: str):
        print(f"{Colors.BLUE}[DEBUG]{Colors.NC} {message}")

class SystemInfo:
    """系统信息检测"""
    
    @staticmethod
    def get_os() -> str:
        """获取操作系统类型"""
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        elif system == 'linux':
            return 'linux'
        else:
            raise Exception(f"不支持的操作系统: {system}")
    
    @staticmethod
    def get_arch() -> str:
        """获取系统架构"""
        machine = platform.machine().lower()
        if machine in ['x86_64', 'amd64']:
            return 'amd64'
        elif machine in ['arm64', 'aarch64']:
            return 'arm64'
        else:
            raise Exception(f"不支持的架构: {machine}")
    
    @staticmethod
    def check_command(command: str) -> bool:
        """检查命令是否存在"""
        return shutil.which(command) is not None

class MihomoInstaller:
    """Mihomo (Clash Meta) 安装器"""
    
    def __init__(self):
        self.logger = Logger()
        self.os_type = SystemInfo.get_os()
        self.arch = SystemInfo.get_arch()
    
    def get_latest_version(self) -> str:
        """获取最新版本号"""
        try:
            self.logger.info("获取Mihomo最新版本...")
            response = requests.get(
                "https://api.github.com/repos/MetaCubeX/mihomo/releases/latest",
                timeout=10
            )
            response.raise_for_status()
            version = response.json()['tag_name']
            self.logger.info(f"最新版本: {version}")
            return version
        except Exception as e:
            self.logger.warn(f"无法获取最新版本: {e}")
            default_version = "v1.19.13"
            self.logger.info(f"使用默认版本: {default_version}")
            return default_version
    
    def get_download_url(self, version: str) -> str:
        """构建下载URL"""
        filename = f"mihomo-{self.os_type}-{self.arch}-compatible-{version}.gz"
        url = f"https://github.com/MetaCubeX/mihomo/releases/download/{version}/{filename}"
        return url
    
    def download_mihomo(self, url: str, dest_path: str) -> bool:
        """下载Mihomo"""
        try:
            self.logger.info(f"下载Mihomo: {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info("下载完成")
            return True
        except Exception as e:
            self.logger.error(f"下载失败: {e}")
            return False
    
    def install(self) -> bool:
        """安装Mihomo"""
        # 检查是否已安装
        if SystemInfo.check_command('clash'):
            self.logger.info("Clash已安装")
            return True
        
        try:
            # 获取版本和下载URL
            version = self.get_latest_version()
            download_url = self.get_download_url(version)
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.gz', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # 下载文件
            if not self.download_mihomo(download_url, temp_path):
                return False
            
            # 解压文件
            self.logger.info("解压文件...")
            binary_path = temp_path[:-3]  # 移除.gz后缀
            with gzip.open(temp_path, 'rb') as f_in:
                with open(binary_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # 设置执行权限
            os.chmod(binary_path, 0o755)
            
            # 移动到系统路径
            install_path = '/usr/local/bin/clash'
            self.logger.info(f"安装到: {install_path}")
            
            # 使用sudo移动文件
            result = subprocess.run(['sudo', 'mv', binary_path, install_path], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"安装失败: {result.stderr}")
                return False
            
            # 清理临时文件
            os.unlink(temp_path)
            
            # 验证安装
            if SystemInfo.check_command('clash'):
                self.logger.info("Mihomo安装成功")
                # 显示版本信息
                result = subprocess.run(['clash', '-v'], capture_output=True, text=True)
                if result.returncode == 0:
                    print(result.stdout.strip())
                return True
            else:
                self.logger.error("安装失败，clash命令不可用")
                return False
                
        except Exception as e:
            self.logger.error(f"安装过程中出错: {e}")
            return False

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.logger = Logger()
        self.config_dir = Path.home() / '.config' / 'clash'
        self.config_file = self.config_dir / 'config.yaml'
        self.project_config = Path('config/clash-config.yaml')
    
    def create_config_dir(self):
        """创建配置目录"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"配置目录: {self.config_dir}")
    
    def load_template_config(self) -> Dict:
        """加载配置模板"""
        if self.project_config.exists():
            with open(self.project_config, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # 返回默认配置
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
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
                    'name': '🚀 节点选择',
                    'type': 'select',
                    'proxies': ['🎯 全球直连']
                },
                {
                    'name': '🎯 全球直连',
                    'type': 'select',
                    'proxies': ['DIRECT']
                }
            ],
            'rules': [
                'DOMAIN-SUFFIX,github.com,🚀 节点选择',
                'DOMAIN-SUFFIX,google.com,🚀 节点选择',
                'GEOIP,CN,🎯 全球直连',
                'MATCH,🚀 节点选择'
            ]
        }
    
    def save_config(self, config: Dict):
        """保存配置"""
        self.create_config_dir()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        self.logger.info(f"配置已保存: {self.config_file}")
    
    def add_shadowsocks_server(self, config: Dict, name: str, server: str, 
                              port: int, password: str, cipher: str = 'aes-256-gcm'):
        """添加Shadowsocks服务器"""
        proxy = {
            'name': name,
            'type': 'ss',
            'server': server,
            'port': port,
            'cipher': cipher,
            'password': password,
            'udp': True
        }
        
        config['proxies'].append(proxy)
        
        # 更新代理组
        for group in config['proxy-groups']:
            if group['name'] == '🚀 节点选择':
                if name not in group['proxies']:
                    group['proxies'].insert(-1, name)  # 在直连前插入
        
        self.logger.info(f"已添加Shadowsocks服务器: {name}")
    
    def add_vmess_server(self, config: Dict, name: str, server: str, port: int, 
                        uuid: str, path: str = '/'):
        """添加VMess服务器"""
        proxy = {
            'name': name,
            'type': 'vmess',
            'server': server,
            'port': port,
            'uuid': uuid,
            'alterId': 0,
            'cipher': 'auto',
            'tls': True,
            'network': 'ws',
            'ws-opts': {
                'path': path,
                'headers': {'Host': server}
            }
        }
        
        config['proxies'].append(proxy)
        
        # 更新代理组
        for group in config['proxy-groups']:
            if group['name'] == '🚀 节点选择':
                if name not in group['proxies']:
                    group['proxies'].insert(-1, name)
        
        self.logger.info(f"已添加VMess服务器: {name}")

class VPNService:
    """VPN服务管理"""
    
    def __init__(self):
        self.logger = Logger()
        self.config_dir = Path.home() / '.config' / 'clash'
        self.config_file = self.config_dir / 'config.yaml'
        self.pid_file = Path('/tmp/clash.pid')
        self.log_file = Path('/tmp/clash.log')
    
    def is_running(self) -> bool:
        """检查服务是否运行"""
        try:
            result = subprocess.run(['pgrep', '-f', 'clash'], 
                                  capture_output=True, text=True)
            return result.returncode == 0 and result.stdout.strip()
        except:
            return False
    
    def get_pid(self) -> Optional[int]:
        """获取进程PID"""
        try:
            result = subprocess.run(['pgrep', '-f', 'clash'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return int(result.stdout.strip().split('\n')[0])
        except:
            pass
        return None
    
    def start(self) -> bool:
        """启动服务"""
        if self.is_running():
            pid = self.get_pid()
            self.logger.warn(f"Clash已在运行 (PID: {pid})")
            return True
        
        if not self.config_file.exists():
            self.logger.error(f"配置文件不存在: {self.config_file}")
            return False
        
        try:
            self.logger.info("启动Clash...")
            
            # 启动clash进程
            with open(self.log_file, 'w') as log_f:
                process = subprocess.Popen(
                    ['clash', '-f', str(self.config_file)],
                    stdout=log_f,
                    stderr=subprocess.STDOUT,
                    start_new_session=True
                )
            
            # 等待一下让进程启动
            import time
            time.sleep(2)
            
            if self.is_running():
                pid = self.get_pid()
                self.logger.info(f"Clash启动成功 (PID: {pid})")
                self.logger.info("HTTP代理: 127.0.0.1:7890")
                self.logger.info("SOCKS代理: 127.0.0.1:7891")
                self.logger.info("控制面板: http://127.0.0.1:9090/ui")
                return True
            else:
                self.logger.error("Clash启动失败")
                return False
                
        except Exception as e:
            self.logger.error(f"启动失败: {e}")
            return False
    
    def stop(self) -> bool:
        """停止服务"""
        pid = self.get_pid()
        if not pid:
            self.logger.warn("Clash未运行")
            return True
        
        try:
            self.logger.info(f"停止Clash (PID: {pid})...")
            os.kill(pid, 15)  # SIGTERM
            
            # 等待进程结束
            import time
            time.sleep(1)
            
            if not self.is_running():
                self.logger.info("Clash已停止")
                return True
            else:
                # 强制终止
                self.logger.warn("强制停止Clash...")
                os.kill(pid, 9)  # SIGKILL
                return True
                
        except Exception as e:
            self.logger.error(f"停止失败: {e}")
            return False
    
    def restart(self) -> bool:
        """重启服务"""
        self.stop()
        import time
        time.sleep(1)
        return self.start()
    
    def status(self):
        """显示服务状态"""
        print("================================")
        print("        VPN服务状态")
        print("================================")
        
        if self.is_running():
            pid = self.get_pid()
            print(f"Clash: {Colors.GREEN}运行中{Colors.NC} (PID: {pid})")
            print("  HTTP代理: 127.0.0.1:7890")
            print("  SOCKS代理: 127.0.0.1:7891")
            print("  控制面板: http://127.0.0.1:9090/ui")
        else:
            print(f"Clash: {Colors.RED}未运行{Colors.NC}")
        
        print("================================")
    
    def test_connection(self):
        """测试网络连接"""
        self.logger.info("测试网络连接...")
        
        # 测试国内网站
        print("测试国内网站 (直连):")
        self._test_url("https://baidu.com", "百度")
        
        print("\n测试国外网站 (代理):")
        # 测试国外网站（通过代理）
        if self.is_running():
            proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890'
            }
            self._test_url("https://google.com", "Google", proxies)
            self._test_url("https://github.com", "GitHub", proxies)
        else:
            print("  代理服务未运行，无法测试")
    
    def _test_url(self, url: str, name: str, proxies: Dict = None):
        """测试单个URL"""
        try:
            response = requests.get(url, proxies=proxies, timeout=10, 
                                  allow_redirects=True)
            if response.status_code == 200:
                print(f"  {name}: {Colors.GREEN}✓{Colors.NC}")
            else:
                print(f"  {name}: {Colors.RED}✗{Colors.NC} (HTTP {response.status_code})")
        except Exception as e:
            print(f"  {name}: {Colors.RED}✗{Colors.NC} ({str(e)})")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='VPN管理工具 - Python版本')
    parser.add_argument('command', nargs='?', default='help',
                       choices=['install', 'start', 'stop', 'restart', 'status', 
                               'test', 'config', 'help'],
                       help='要执行的命令')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        print_help()
    elif args.command == 'install':
        installer = MihomoInstaller()
        if installer.install():
            print("\n安装完成！接下来请运行:")
            print("  python3 vpn_manager.py config  # 配置服务器")
            print("  python3 vpn_manager.py start   # 启动服务")
    elif args.command == 'config':
        configure_servers()
    elif args.command == 'start':
        service = VPNService()
        service.start()
    elif args.command == 'stop':
        service = VPNService()
        service.stop()
    elif args.command == 'restart':
        service = VPNService()
        service.restart()
    elif args.command == 'status':
        service = VPNService()
        service.status()
    elif args.command == 'test':
        service = VPNService()
        service.test_connection()

def print_help():
    """显示帮助信息"""
    print("VPN管理工具 - Python版本")
    print()
    print("用法: python3 vpn_manager.py [命令]")
    print()
    print("命令:")
    print("  install    安装Mihomo (Clash Meta)")
    print("  config     配置服务器信息")
    print("  start      启动VPN服务")
    print("  stop       停止VPN服务")
    print("  restart    重启VPN服务")
    print("  status     查看服务状态")
    print("  test       测试网络连接")
    print("  help       显示帮助")
    print()
    print("示例:")
    print("  python3 vpn_manager.py install")
    print("  python3 vpn_manager.py config")
    print("  python3 vpn_manager.py start")

def configure_servers():
    """配置服务器"""
    config_manager = ConfigManager()
    logger = Logger()
    
    # 加载现有配置
    config = config_manager.load_template_config()
    
    print("================================")
    print("        VPN服务器配置")
    print("================================")
    print("1) 配置Shadowsocks服务器")
    print("2) 配置VMess服务器")
    print("3) 保存并退出")
    print("================================")
    
    while True:
        try:
            choice = input("请选择 [3]: ").strip() or "3"
            
            if choice == "1":
                configure_shadowsocks(config, config_manager)
            elif choice == "2":
                configure_vmess(config, config_manager)
            elif choice == "3":
                config_manager.save_config(config)
                logger.info("配置完成！")
                print("\n使用方法:")
                print("  python3 vpn_manager.py start   # 启动服务")
                print("  python3 vpn_manager.py test    # 测试连接")
                break
            else:
                print("无效选择，请重试")
        except KeyboardInterrupt:
            print("\n\n配置已取消")
            break

def configure_shadowsocks(config: Dict, config_manager: ConfigManager):
    """配置Shadowsocks服务器"""
    print("\n配置Shadowsocks服务器:")
    print("--------------------------------")
    
    try:
        name = input("服务器名称 [SS-Server]: ").strip() or "SS-Server"
        server = input("服务器地址: ").strip()
        if not server:
            print("服务器地址不能为空")
            return
        
        port_str = input("端口 [443]: ").strip() or "443"
        try:
            port = int(port_str)
        except ValueError:
            print("端口必须是数字")
            return
        
        password = input("密码: ").strip()
        if not password:
            print("密码不能为空")
            return
        
        print("加密方式:")
        print("1) aes-256-gcm (推荐)")
        print("2) aes-128-gcm")
        print("3) chacha20-ietf-poly1305")
        cipher_choice = input("选择加密方式 [1]: ").strip() or "1"
        
        cipher_map = {
            "1": "aes-256-gcm",
            "2": "aes-128-gcm", 
            "3": "chacha20-ietf-poly1305"
        }
        cipher = cipher_map.get(cipher_choice, "aes-256-gcm")
        
        config_manager.add_shadowsocks_server(config, name, server, port, password, cipher)
        print(f"✓ 已添加Shadowsocks服务器: {name}")
        
    except KeyboardInterrupt:
        print("\n配置已取消")

def configure_vmess(config: Dict, config_manager: ConfigManager):
    """配置VMess服务器"""
    print("\n配置VMess服务器:")
    print("--------------------------------")
    
    try:
        name = input("服务器名称 [VMess-Server]: ").strip() or "VMess-Server"
        server = input("服务器地址: ").strip()
        if not server:
            print("服务器地址不能为空")
            return
        
        port_str = input("端口 [443]: ").strip() or "443"
        try:
            port = int(port_str)
        except ValueError:
            print("端口必须是数字")
            return
        
        uuid = input("UUID: ").strip()
        if not uuid:
            # 生成UUID
            import uuid as uuid_module
            uuid = str(uuid_module.uuid4())
            print(f"已生成UUID: {uuid}")
        
        path = input("WebSocket路径 [/]: ").strip() or "/"
        
        config_manager.add_vmess_server(config, name, server, port, uuid, path)
        print(f"✓ 已添加VMess服务器: {name}")
        
    except KeyboardInterrupt:
        print("\n配置已取消")

if __name__ == "__main__":
    main()