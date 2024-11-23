import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import json


class Toplevel1:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("600x109")
        top.title("Video Repair")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Text1 = tk.Text(top)
        self.Text1.place(relx=0.133, rely=0.092, relheight=0.202, relwidth=0.823)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(width=494)
        self.Text1.configure(wrap='word')

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.017, rely=0.092, height=23, width=55)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''old path''')

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.133, rely=0.459, height=28, width=100)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''读取视频''')
        self.Button1.config(command=self.load_video)

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.33, rely=0.459, height=28, width=100)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''修复视频''')
        self.Button2.config(command=self.repair_video)

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.583, rely=0.505, height=23, width=117)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''''')

        self.video_path = ""  # 存储视频文件路径

    def load_video(self):
        self.video_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv")],
            title="Select a video file"
        )
        if self.video_path:
            self.Text1.delete(1.0, tk.END)  # 清空文本框
            self.Text1.insert(tk.END, self.video_path)  # 显示视频文件路径

    def repair_video(self):
        if not self.video_path:
            messagebox.showwarning("Warning", "Please load a video file first.")
            return  # 如果没有选择视频文件，不执行修复操作

        self.Label2.configure(text="Repairing...")
        self.Label2.update()

        # 创建线程执行视频修复命令
        threading.Thread(target=self.run_ffmpeg).start()

    def run_ffmpeg(self):
        # 获取视频的帧率
        framerate = self.get_framerate(self.video_path)

        # 构建ffmpeg命令
        video_dir = os.path.dirname(self.video_path)
        fixed_video_filename = os.path.splitext(os.path.basename(self.video_path))[0] + "_fixed.mp4"
        fixed_video_path = os.path.join(video_dir, fixed_video_filename)
        command = ["ffmpeg", "-i", self.video_path, "-vcodec", "libx264", "-crf", "17", "-c:a", "copy", "-r",
                   str(framerate), fixed_video_path]

        try:
            subprocess.run(command, check=True)
            self.update_label("Repaired")
            self.show_result(fixed_video_path)
        except subprocess.CalledProcessError as e:
            self.update_label("Error")
            self.show_error(e)

    def get_framerate(self, video_path):
        # 使用ffprobe获取视频的帧率
        command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of",
                   "json", video_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        framerate_json = json.loads(result.stdout.decode())
        framerate = framerate_json["streams"][0]["r_frame_rate"]
        return framerate

    def update_label(self, text):
        self.Label2.configure(text=text)
        self.Label2.update()

    def show_result(self, fixed_video_path):
        messagebox.showinfo("Info", f"Video repaired successfully. Saved as: {fixed_video_path}")

    def show_error(self, e):
        messagebox.showerror("Error", f"An error occurred: {e}")

def center_window(window, width, height):
    """Center the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def vp_start_gui():
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    center_window(root, 600, 109)
    root.mainloop()


if __name__ == '__main__':
    vp_start_gui()