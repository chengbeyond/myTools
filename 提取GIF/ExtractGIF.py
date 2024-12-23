import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os


def extract_frames_from_gif(gif_path, output_folder):
    gif = Image.open(gif_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame = 0
    while True:
        try:
            gif.seek(frame)
            gif.save(os.path.join(output_folder, f"frame_{frame}.png"))
            frame += 1
        except EOFError:
            break


def select_gif_file():
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        gif_path_var.set(file_path)


def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_var.set(folder_path)


def extract_frames():
    gif_path = gif_path_var.get()
    output_folder = output_folder_var.get()
    if gif_path and output_folder:
        extract_frames_from_gif(gif_path, output_folder)
        messagebox.showinfo("Success", "Frames extracted successfully!")
    else:
        messagebox.showwarning("Warning", "Please select both GIF file and output folder.")


# 创建主窗口
root = tk.Tk()
root.title("GIF Frame Extractor")

gif_path_var = tk.StringVar()
output_folder_var = tk.StringVar()

# 创建一个框架用于GIF文件选择部分
gif_frame = tk.Frame(root)
gif_frame.pack(pady=10)

tk.Label(gif_frame, text="GIF File:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(gif_frame, textvariable=gif_path_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(gif_frame, text="Select GIF File", command=select_gif_file).grid(row=0, column=2, padx=5, pady=5)

# 创建一个框架用于输出文件夹选择部分
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

tk.Label(output_frame, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(output_frame, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(output_frame, text="Select Output Folder", command=select_output_folder).grid(row=1, column=2, padx=5, pady=5)

# 创建并放置提取帧的按钮
tk.Button(root, text="Extract Frames", command=extract_frames).pack(pady=20)


# 设置窗口位置居中
def center_window(root):
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')


root.update_idletasks()  # 更新窗口尺寸信息
center_window(root)  # 初始化时居中一次

# 运行主循环
root.mainloop()
