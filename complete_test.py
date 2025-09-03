#!/usr/bin/env python3
"""
完整的VPN测试和验证工具
"""

import subprocess
import requests
import time
import json
from pathlib import Path

class VPNTester:
    def __init__(self):
        self.proxy_http = "http://127.0.0.1:7890"
        self.proxy_socks = "socks5://127.0.0.1:7891"
        self.control_url = "http://127.0.0.1:9090"
        
    def test_clash_status(self):
        """测试Clash服务状态"""
        print("🔍 检查Clash服务状态...")
        try:
            result = subprocess.run(['python3', 'vpn_manager.py', 'status'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Clash服务正在运行")
                return True
            else:
                print("❌ Clash服务未运行")
                return False
        except Exception as e:
            print(f"❌ 检查服务状态失败: {e}")
            return False
    
    def test_proxy_connectivity(self):
        """测试代理连接性"""
        print("\n🌐 测试代理连接性...")
        
        # 测试HTTP代理
        try:
            proxies = {'http': self.proxy_http, 'https': self.proxy_http}
            response = requests.get('http://httpbin.org/ip', 
                                  proxies=proxies, timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ HTTP代理连接成功，IP: {ip_info.get('origin', 'Unknown')}")
                return True
        except Exception as e:
            print(f"❌ HTTP代理连接失败: {e}")
            
        return False
    
    def test_direct_connection(self):
        """测试直连"""
        print("\n🔗 测试直连...")
        try:
            response = requests.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                ip_info = response.json()
                print(f"✅ 直连成功，IP: {ip_info.get('origin', 'Unknown')}")
                return True
        except Exception as e:
            print(f"❌ 直连失败: {e}")
            return False
    
    def test_clash_api(self):
        """测试Clash API"""
        print("\n🎛️ 测试Clash控制API...")
        try:
            response = requests.get(f"{self.control_url}/version", timeout=5)
            if response.status_code == 200:
                version_info = response.json()
                print(f"✅ Clash API响应正常")
                print(f"   版本: {version_info.get('version', 'Unknown')}")
                return True
        except Exception as e:
            print(f"❌ Clash API连接失败: {e}")
            return False
    
    def test_dns_resolution(self):
        """测试DNS解析"""
        print("\n🔍 测试DNS解析...")
        test_domains = [
            'www.google.com',
            'github.com',
            'www.baidu.com',
            'www.taobao.com'
        ]
        
        success_count = 0
        for domain in test_domains:
            try:
                import socket
                socket.gethostbyname(domain)
                print(f"✅ {domain} 解析成功")
                success_count += 1
            except Exception as e:
                print(f"❌ {domain} 解析失败: {e}")
        
        return success_count == len(test_domains)
    
    def test_speed(self):
        """测试网络速度"""
        print("\n⚡ 测试网络速度...")
        
        test_urls = [
            ('直连测试', 'http://www.baidu.com', None),
            ('代理测试', 'http://www.google.com', 
             {'http': self.proxy_http, 'https': self.proxy_http})
        ]
        
        for name, url, proxies in test_urls:
            try:
                start_time = time.time()
                response = requests.get(url, proxies=proxies, timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    speed = end_time - start_time
                    print(f"✅ {name}: {speed:.2f}秒")
                else:
                    print(f"❌ {name}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: {e}")
    
    def test_specific_sites(self):
        """测试特定网站访问"""
        print("\n🌍 测试特定网站访问...")
        
        # 国外网站（应该通过代理）
        foreign_sites = [
            ('Google', 'https://www.google.com'),
            ('GitHub', 'https://github.com'),
            ('YouTube', 'https://www.youtube.com')
        ]
        
        # 国内网站（应该直连）
        domestic_sites = [
            ('百度', 'https://www.baidu.com'),
            ('淘宝', 'https://www.taobao.com'),
            ('腾讯', 'https://www.qq.com')
        ]
        
        print("  国外网站（通过代理）:")
        proxies = {'http': self.proxy_http, 'https': self.proxy_http}
        for name, url in foreign_sites:
            try:
                response = requests.get(url, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    print(f"    ✅ {name}: 访问成功")
                else:
                    print(f"    ❌ {name}: HTTP {response.status_code}")
            except Exception as e:
                print(f"    ❌ {name}: {e}")
        
        print("  国内网站（直连）:")
        for name, url in domestic_sites:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"    ✅ {name}: 访问成功")
                else:
                    print(f"    ❌ {name}: HTTP {response.status_code}")
            except Exception as e:
                print(f"    ❌ {name}: {e}")
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*50)
        print("           VPN系统测试报告")
        print("="*50)
        
        tests = [
            ("Clash服务状态", self.test_clash_status),
            ("代理连接性", self.test_proxy_connectivity),
            ("直连测试", self.test_direct_connection),
            ("Clash API", self.test_clash_api),
            ("DNS解析", self.test_dns_resolution)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name}测试异常: {e}")
                results[test_name] = False
        
        # 运行速度和网站测试
        self.test_speed()
        self.test_specific_sites()
        
        # 总结
        print("\n" + "="*50)
        print("           测试结果总结")
        print("="*50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name}: {status}")
        
        print(f"\n总体结果: {passed}/{total} 项测试通过")
        
        if passed == total:
            print("🎉 所有测试通过！VPN系统运行正常")
        else:
            print("⚠️  部分测试失败，请检查配置")
        
        return passed == total

def main():
    """主函数"""
    print("🚀 开始VPN系统完整测试...")
    
    tester = VPNTester()
    success = tester.generate_report()
    
    if success:
        print("\n✅ VPN系统测试完成，一切正常！")
        print("💡 你现在可以:")
        print("   - 访问 http://127.0.0.1:9090/ui 查看Clash控制面板")
        print("   - 使用代理: HTTP 127.0.0.1:7890, SOCKS 127.0.0.1:7891")
        print("   - 运行 python3 vpn_manager.py help 查看管理命令")
    else:
        print("\n❌ 部分测试失败，请检查配置或重新安装")
        print("💡 故障排除:")
        print("   - 运行 python3 vpn_manager.py restart 重启服务")
        print("   - 检查配置文件 ~/.config/clash/config.yaml")
        print("   - 查看日志文件了解详细错误信息")

if __name__ == "__main__":
    main()