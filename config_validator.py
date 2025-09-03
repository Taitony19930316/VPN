#!/usr/bin/env python3
"""
配置文件验证工具
"""

import yaml
import json
import sys
from pathlib import Path

def validate_clash_config(config_path: str):
    """验证Clash配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print(f"✓ 配置文件语法正确: {config_path}")
        
        # 检查必要字段
        required_fields = ['port', 'socks-port', 'proxies', 'proxy-groups', 'rules']
        missing_fields = []
        
        for field in required_fields:
            if field not in config:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"✗ 缺少必要字段: {missing_fields}")
            return False
        
        # 检查代理服务器
        proxies = config.get('proxies', [])
        if not proxies:
            print("⚠ 警告: 没有配置代理服务器")
        else:
            print(f"✓ 找到 {len(proxies)} 个代理服务器:")
            for proxy in proxies:
                name = proxy.get('name', '未命名')
                proxy_type = proxy.get('type', '未知')
                server = proxy.get('server', '未配置')
                print(f"  - {name} ({proxy_type}): {server}")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"✗ YAML语法错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 配置文件错误: {e}")
        return False

def main():
    """主函数"""
    config_files = [
        'config/clash-config.yaml',
        'config/test-config.yaml',
        Path.home() / '.config' / 'clash' / 'config.yaml'
    ]
    
    print("配置文件验证工具")
    print("=" * 40)
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"\n检查: {config_file}")
            validate_clash_config(str(config_file))
        else:
            print(f"\n跳过: {config_file} (文件不存在)")

if __name__ == "__main__":
    main()