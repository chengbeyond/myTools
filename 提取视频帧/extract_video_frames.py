import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import threading
from PIL import Image
import subprocess

pause_event = threading.Event()
pause_event.set()


def select_video():
    video_path = filedialog.askopenfilename()
    if video_path:
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(0, video_path)
        # 获取并显示视频的总帧数
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        root.title(f"视频帧提取工具 - 总帧数: {total_frames}")


def select_output_folder():
    output_folder = filedialog.askdirectory()
    if output_folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, output_folder)


def extract_frames():
    video_path = video_path_entry.get()
    output_folder = output_folder_entry.get()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not cap.isOpened():
        print("无法打开视频文件")
        return

    frame_count = 0
    while True:
        pause_event.wait()  # 等待继续信号
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"frame_{frame_count:05d}.png")
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        pil_img.save(frame_path)

        frame_count += 1
        progress_label.config(text=f"进度: {frame_count}/{total_frames} 帧")

    cap.release()
    status_label.config(text=f"提取的帧数: {frame_count}")

    # 弹出完成提示框
    messagebox.showinfo("完成", f"提取完成！总计提取了 {frame_count} 帧。")
    # 打开输出文件夹
    open_output_folder(output_folder)


def open_output_folder(folder_path):
    if os.name == 'nt':  # Windows
        os.startfile(folder_path)
    elif os.name == 'posix':  # macOS, Linux
        subprocess.run(['open', folder_path] if sys.platform == 'darwin' else ['xdg-open', folder_path])


def start_extraction():
    extraction_thread = threading.Thread(target=extract_frames)
    extraction_thread.start()


def toggle_pause():
    if pause_event.is_set():
        pause_event.clear()
        pause_button.config(text="继续提取")
    else:
        pause_event.set()
        pause_button.config(text="暂停提取")


def center_window(root, width=550, height=330):
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


root = tk.Tk()
root.title("视频帧提取工具")

# 设置窗口大小和居中
center_window(root, 550, 200)

# 创建和布局组件
tk.Label(root, text="视频路径:").grid(row=0, column=0, padx=10, pady=10)
video_path_entry = tk.Entry(root, width=50)
video_path_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="选择视频", command=select_video).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="输出路径:").grid(row=1, column=0, padx=10, pady=10)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="保存路径", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="提取视频帧", command=start_extraction).grid(row=2, column=1, padx=10, pady=10)

pause_button = tk.Button(root, text="暂停提取", command=toggle_pause)
pause_button.grid(row=2, column=2, padx=10, pady=10)

progress_label = tk.Label(root, text="进度: 0/0 帧")
progress_label.grid(row=3, column=1, padx=10, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
