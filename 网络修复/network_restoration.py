import platform
import subprocess
import requests
import ctypes
import sys
import os


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        # 重新启动脚本并请求管理员权限
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)


def test_network_connection():
    try:
        response = requests.get('http://www.baidu.com', timeout=5)
        if response.status_code == 200:
            print("网络连接正常")
            return True
    except requests.RequestException as e:
        print(f"网络连接失败: {e}")

    try:
        output = subprocess.run(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if output.returncode == 0:
            print("Ping成功")
            return True
        else:
            print("Ping失败")
            return False
    except requests.RequestException as e:
        print(f"网络连接失败: {e}")


def clear_dns_cache():
    os_name = platform.system().lower()

    if os_name == 'windows':
        print("正在清理Windows DNS缓存...")
        subprocess.run(['ipconfig', '/flushdns'])

    elif os_name == 'linux':
        print("正在清理Linux DNS缓存...")
        subprocess.run(['sudo', 'systemd-resolve', '--flush-caches'])

    else:
        print("不支持的操作系统")


def reset_network():
    os_name = platform.system().lower()

    if os_name == 'windows':
        print("正在重置Windows网络...")
        subprocess.run(['netsh', 'winsock', 'reset'])
        subprocess.run(['ipconfig', '/release'])
        subprocess.run(['ipconfig', '/renew'])

    elif os_name == 'linux':
        print("正在重置Linux网络...")
        subprocess.run(['sudo', 'service', 'network-manager', 'restart'])

    else:
        print("不支持的操作系统")


def main():
    if not test_network_connection():
        print("网络不通，尝试清理DNS缓存并重置网络...")
        reset_network()
        clear_dns_cache()


if __name__ == "__main__":
    if platform.system().lower() == 'windows':
        run_as_admin()  # 在Windows上尽早尝试获取管理员权限
    main()
    # 等待用户按下任意键后退出
    input("按任意键退出...")
