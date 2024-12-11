import os
import threading
from tkinter import Tk, Label, Entry, Button, Frame, filedialog, messagebox
from PIL import Image

def select_input_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, 'end')
    entry.insert(0, folder_selected)

def select_output_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, 'end')
    entry.insert(0, folder_selected)

def change_shadow_color(image_path, output_path, old_color, new_color):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []

    for item in datas:
        if item[:3] == old_color[:3]:
            new_data.append((new_color[0], new_color[1], new_color[2], item[3]))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path)

def update_progress_label(current, total):
    progress_label.config(text=f"处理进度: {current}/{total}")

def process_images_in_folder():
    input_folder = input_entry.get()
    output_folder = output_entry.get()
    old_color = (15, 127, 37)  # 绿色 #0F7F25
    new_color = (60, 60, 60)  # 淡黑色

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    total_images = len(image_files)

    for i, filename in enumerate(image_files, start=1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f'processed_{filename}')
        change_shadow_color(input_path, output_path, old_color, new_color)
        update_progress_label(i, total_images)

    messagebox.showinfo("处理完成", "所有图片已处理完成！")

def start_processing():
    processing_thread = threading.Thread(target=process_images_in_folder)
    processing_thread.start()

# 创建主窗口
root = Tk()
root.title("像素影子处理")

# 设置窗口大小
window_width = 580
window_height = 160  # 增加窗口高度以容纳进度标签

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口位置
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口位置
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 输入文件夹路径
Label(root, text="输入文件夹路径:").grid(row=0, column=0, padx=10, pady=10)
input_entry = Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="选择路径", command=lambda: select_input_folder(input_entry)).grid(row=0, column=2, padx=10, pady=10)

# 输出文件夹路径
Label(root, text="输出文件夹路径:").grid(row=1, column=0, padx=10, pady=10)
output_entry = Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="选择路径", command=lambda: select_output_folder(output_entry)).grid(row=1, column=2, padx=10, pady=10)

# 进度标签
progress_label = Label(root, text="处理进度: 0/0")
progress_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)

# 处理图片按钮和选择文件夹按钮
button_frame = Frame(root)  # 修正这里，直接使用 Frame 而不是 Tk.Frame
button_frame.grid(row=2, column=1, columnspan=2, sticky='e', padx=10, pady=10)

Button(button_frame, text="处理图片", command=start_processing).pack(side='right', padx=0)

# 运行主循环
root.mainloop()
