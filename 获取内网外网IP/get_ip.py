import tkinter as tk
from tkinter import messagebox
import socket
import requests
import threading

# 全局变量用于存储状态
is_fetching = False

def get_local_ip():
    try:
        # 获取内网 IP 地址
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"获取内网 IP 地址时出错: {e}")
        return "无法获取"

def get_public_ip():
    try:
        # 获取外网 IP 地址
        response = requests.get("https://ipinfo.io/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('ip', "无法获取")
        else:
            return "无法获取"
    except Exception as e:
        print(f"获取外网 IP 地址时出错: {e}")
        return "无法获取"

def start_ip_fetch():
    global is_fetching
    if is_fetching:
        messagebox.showinfo("提示", "正在获取 IP 地址，请稍候...")
        return
    is_fetching = True
    local_ip_box.config(state=tk.NORMAL)
    public_ip_box.config(state=tk.NORMAL)
    local_ip_box.delete('1.0', tk.END)
    public_ip_box.delete('1.0', tk.END)
    local_ip_box.insert(tk.END, "获取中...")
    public_ip_box.insert(tk.END, "获取中...")
    local_ip_box.config(state=tk.DISABLED)
    public_ip_box.config(state=tk.DISABLED)

    # 启动线程异步获取 IP
    threading.Thread(target=fetch_ip).start()

def fetch_ip():
    global is_fetching

    # 获取内网 IP 地址
    local_ip = get_local_ip()
    local_ip_box.config(state=tk.NORMAL)
    local_ip_box.delete('1.0', tk.END)
    local_ip_box.insert(tk.END, local_ip)
    local_ip_box.config(state=tk.DISABLED)

    # 获取外网 IP 地址
    public_ip = get_public_ip()
    public_ip_box.config(state=tk.NORMAL)
    public_ip_box.delete('1.0', tk.END)
    public_ip_box.insert(tk.END, public_ip)
    public_ip_box.config(state=tk.DISABLED)

    # 任务完成
    is_fetching = False

def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算窗口左上角的位置
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口位置
    window.geometry(f'{width}x{height}+{x}+{y}')

def enable_copy(event):
    event.widget.config(state=tk.NORMAL)
    try:
        event.widget.tag_add(tk.SEL, "1.0", tk.END)
        event.widget.mark_set(tk.INSERT, "1.0")
        event.widget.clipboard_clear()
        event.widget.clipboard_append(event.widget.selection_get())
    except tk.TclError:
        pass
    finally:
        event.widget.config(state=tk.DISABLED)

def copy_text(widget):
    widget.config(state=tk.NORMAL)
    try:
        widget.clipboard_clear()
        widget.clipboard_append(widget.selection_get())
    except tk.TclError:
        pass
    finally:
        widget.config(state=tk.DISABLED)

def show_context_menu(event):
    context_menu.entryconfigure("复制", command=lambda: copy_text(event.widget))
    context_menu.post(event.x_root, event.y_root)

# 创建主窗口
root = tk.Tk()
root.title("IP 地址获取器")

# 设置窗口大小
window_width = 320
window_height = 140

# 将窗口居中
center_window(root, window_width, window_height)

# 创建上下文菜单
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="复制", command=None)

# 添加文本标签和输入框
tk.Label(root, text="内网地址：").place(x=10, y=10)
local_ip_box = tk.Text(root, width=25, height=1, state=tk.DISABLED)
local_ip_box.place(x=100, y=10)
local_ip_box.bind("<Control-c>", enable_copy)
local_ip_box.bind("<Button-3>", show_context_menu)

tk.Label(root, text="外网地址：").place(x=10, y=50)
public_ip_box = tk.Text(root, width=25, height=1, state=tk.DISABLED)
public_ip_box.place(x=100, y=50)
public_ip_box.bind("<Control-c>", enable_copy)
public_ip_box.bind("<Button-3>", show_context_menu)

# 添加按钮
fetch_button = tk.Button(root, text="获取 IP 地址", width=15, command=start_ip_fetch)
fetch_button.place(x=10, y=90)

# 运行主循环
root.mainloop()
