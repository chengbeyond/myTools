import os
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading
import configparser
import subprocess

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CONFIG_FILE = 'translation_config.ini'

def save_config(input_dir, output_dir):
    config = configparser.ConfigParser()
    config['Paths'] = {
        'input_dir': input_dir,
        'output_dir': output_dir
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'Paths' in config:
            return config['Paths'].get('input_dir', ''), config['Paths'].get('output_dir', '')
    return '', ''

def translate_text_file(input_file_path, output_dir):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    url = "https://deeplx.doi9.top/translate"
    payload = json.dumps({
        "text": content,
        "source_lang": "auto",
        "target_lang": "ZH"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    data_dict = response.json()

    # 获取输入文件名并构造输出文件路径
    input_filename = os.path.basename(input_file_path)
    output_file_path = os.path.join(output_dir, input_filename.replace('.', '_translated.'))

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(data_dict.get("data"))

    print(f"数据已成功写入到 {output_file_path}")
    return 1  # 返回1表示完成一个文件的翻译

def process_directory(input_dir, output_dir, progress_var, total_files):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    translated_count = 0
    for filename in os.listdir(input_dir):
        if filename.endswith(('.txt', '.srt', '.docx', '.md')):  # 添加更多文本文件扩展名
            input_file_path = os.path.join(input_dir, filename)
            translated_count += translate_text_file(input_file_path, output_dir)
            remaining_files = total_files - translated_count
            progress_var.set(f"翻译进度: {translated_count}/{total_files} 文件完成 (剩余: {remaining_files})")
            root.update_idletasks()  # 更新UI以显示进度

    messagebox.showinfo("完成", "翻译完成")
    # 打开翻译好的目录
    open_folder(output_dir)

def open_folder(folder_path):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(folder_path)
        elif os.name == 'posix':  # Linux 或 macOS
            subprocess.Popen(['open', folder_path])
        else:
            messagebox.showwarning("警告", "无法在当前操作系统上打开文件夹")
    except Exception as e:
        messagebox.showerror("错误", f"打开文件夹时出错: {e}")

def select_input_directory():
    directory = filedialog.askdirectory()
    if directory:
        input_path_entry.delete(0, tk.END)
        input_path_entry.insert(0, directory)

def select_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, directory)

def start_translation():
    input_dir = input_path_entry.get()
    output_dir = output_path_entry.get()

    if not input_dir or not output_dir:
        messagebox.showwarning("警告", "请输入输入目录和输出目录")
        return

    # 计算总文件数
    total_files = sum(1 for filename in os.listdir(input_dir) if filename.endswith('.srt'))
    if total_files == 0:
        messagebox.showwarning("警告", "输入目录中没有 .srt 文件")
        return

    # 保存配置
    save_config(input_dir, output_dir)

    # 修改按钮文本为“翻译中”
    translate_button.config(text="正在翻译", state=tk.DISABLED)

    # 创建进度变量
    progress_var = tk.StringVar()
    progress_var.set("翻译准备中...")
    progress_label = tk.Label(root, textvariable=progress_var)
    progress_label.grid(row=2, column=1, padx=(10, 0), pady=20, sticky=tk.W)  # 紧靠开始翻译按钮后面10个像素的地方

    # 启动新线程进行翻译
    translation_thread = threading.Thread(target=process_directory, args=(input_dir, output_dir, progress_var, total_files))
    translation_thread.start()

    # 监听线程结束
    def check_thread():
        if translation_thread.is_alive():
            root.after(100, check_thread)  # 每100毫秒检查一次
        else:
            translate_button.config(text="开始翻译", state=tk.NORMAL)  # 启用按钮并恢复文本
            progress_label.destroy()  # 移除进度标签

    check_thread()

# 创建主窗口
root = tk.Tk()
root.title("SRT 文件翻译工具")

# 设置窗口大小
window_width = 550
window_height = 160

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口左上角的位置
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口位置
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 加载配置
input_dir, output_dir = load_config()

# 输入路径部分
input_path_label = tk.Label(root, text="输入路径:")
input_path_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

input_path_entry = tk.Entry(root, width=50)
input_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
input_path_entry.insert(0, input_dir)  # 填充输入路径

select_input_button = tk.Button(root, text="选择目录", command=select_input_directory)
select_input_button.grid(row=0, column=2, padx=10, pady=5, sticky=tk.E)

# 输出路径部分
output_path_label = tk.Label(root, text="输出路径:")
output_path_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

output_path_entry = tk.Entry(root, width=50)
output_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
output_path_entry.insert(0, output_dir)  # 填充输出路径

select_output_button = tk.Button(root, text="选择目录", command=select_output_directory)
select_output_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.E)

# 翻译按钮
translate_button = tk.Button(root, text="开始翻译", command=start_translation)
translate_button.grid(row=2, column=2, padx=10, pady=20)

# 运行主循环
root.mainloop()
