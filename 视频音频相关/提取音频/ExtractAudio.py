import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os


class Toplevel1:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("600x109")
        top.title("提取音频")
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
        self.Label1.configure(text='''路径''')

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.133, rely=0.459, height=28, width=90)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''读取视频文件''')
        self.Button1.config(command=self.load_video)

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.3, rely=0.459, height=28, width=79)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''提取音频''')
        self.Button2.config(command=self.extract_audio)

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.483, rely=0.505, height=23, width=117)
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

    def extract_audio(self):
        if not self.video_path:
            messagebox.showwarning("Warning", "Please load a video file first.")
            return  # 如果没有选择视频文件，不执行提取操作

        self.Label2.configure(text="提取中...")
        self.Label2.update()

        # 构建ffmpeg命令
        video_dir = os.path.dirname(self.video_path)
        audio_filename = os.path.splitext(os.path.basename(self.video_path))[0] + ".wav"
        audio_path = os.path.join(video_dir, audio_filename)
        command = ["ffmpeg", "-i", self.video_path, "-vn", "-acodec", "pcm_s16le", audio_path]

        # 调用ffmpeg提取音频
        try:
            subprocess.run(command, check=True)
            self.Label2.configure(text="提取完成")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.Label2.configure(text="Error")


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
