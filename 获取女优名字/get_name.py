import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk
import threading

def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 390
    window_height = 220
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"+{x}+{y}")
def process_input():
    input_text = entry.get().strip()
    if not input_text:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "请输入女优名")
        return

    def background_task():
        try:
            url = f"https://www.javbus.com/{input_text}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }

            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "正在查询...\n")

            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                container_div = soup.find('div', class_='container')
                if container_div:
                    star_name_divs = container_div.find_all('div', class_='star-name')
                    if star_name_divs:
                        result_text.delete(1.0, tk.END)
                        for div in star_name_divs:
                            result_text.insert(tk.END, f"{div.get_text(strip=True)}\n")
                    else:
                        result_text.delete(1.0, tk.END)
                        result_text.insert(tk.END, "没有找到类名为star-name的<div>")
                else:
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, "没有找到类名为container的<div>")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"发生错误: {str(e)}")

    thread = threading.Thread(target=background_task)
    thread.start()

root = tk.Tk()
root.title("番号查询女优")
root.geometry("390x220")
center_window(root)

entry_label = ttk.Label(root, text="请输入番号:")
entry_label.pack(pady=10)
entry = ttk.Entry(root, width=50)
entry.pack(pady=5)

button = ttk.Button(root, text="查询女优名", command=process_input)
button.pack(pady=10)

result_text = tk.Text(root, height=15, width=50)
result_text.pack(pady=10)

root.mainloop()
