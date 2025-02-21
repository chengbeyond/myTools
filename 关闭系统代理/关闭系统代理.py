import tkinter as tk
from tkinter import messagebox
import winreg
import os
import sys
import ctypes  # 导入 ctypes

def is_admin():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def disable_proxy():
    try:
        # 注册表路径
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

        # 连接到HKEY_CURRENT_USER
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_ALL_ACCESS)

        # 禁用代理
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

        # 删除ProxyServer的值
        try:
            winreg.DeleteValue(key, "ProxyServer")
        except FileNotFoundError:
            pass  # 如果ProxyServer不存在，则忽略

        # 删除AutoConfigURL的值
        try:
            winreg.DeleteValue(key, "AutoConfigURL")
        except FileNotFoundError:
            pass  # 如果AutoConfigURL不存在，则忽略

        # 关闭注册表
        winreg.CloseKey(key)

        # 刷新Internet设置，使更改生效
        INTERNET_OPTION_SETTINGS_CHANGED = 39
        INTERNET_OPTION_REFRESH = 37
        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
        internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
        internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)

        messagebox.showinfo("Success", "代理已禁用！")

    except Exception as e:
        messagebox.showerror("Error", f"禁用代理时出错：{str(e)}")

def run_as_admin():
    import sys
    import ctypes
    # 使用 ctypes 检查是否具有管理员权限
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # 如果没有管理员权限，则使用管理员权限重新启动脚本
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def main():
    root = tk.Tk()
    root.title("禁用代理")
    root.geometry("300x150")

    button = tk.Button(root, text="禁用代理", command=disable_proxy, width=20, height=2)
    button.pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
     # 检查是否以管理员身份运行
    try:
        if not is_admin():
            run_as_admin()
        else:
            main()
    except Exception as e:
        print(f"发生错误: {e}")
        input("按任意键退出...")
