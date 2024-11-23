import tkinter as tk
from tkinter import filedialog
import subprocess
import threading

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

import incorporation_support


def select_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if file_path:
        app.Text1.delete(1.0, tk.END)
        app.Text1.insert(tk.END, file_path)


def select_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
    if file_path:
        app.Text2.delete(1.0, tk.END)
        app.Text2.insert(tk.END, file_path)


def merge_video_audio():
    video_path = app.Text1.get(1.0, tk.END).strip()
    audio_path = app.Text2.get(1.0, tk.END).strip()
    if not video_path or not audio_path:
        return  # 如果没有选择文件，则不执行任何操作

    app.Button3.config(text="合并中...")

    command = ['ffmpeg', '-i', video_path, '-i', audio_path, '-vcodec', 'copy', '-acodec', 'copy', 'output.mp4']

    def run_command():
        try:
            subprocess.run(command, check=True)
            print("Merge completed.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while merging: {e}")
        finally:
            app.Button3.config(text="合并视频和音频")

    thread = threading.Thread(target=run_command)
    thread.start()


def vp_start_gui():
    global val, w, root, app
    root = tk.Tk()
    app = Toplevel1(root)
    incorporation_support.init(root, app)
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    app = Toplevel1(w)
    incorporation_support.init(w, app, *args, **kwargs)
    return (w, app)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("600x144+579+156")
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.Text1 = tk.Text(top)
        self.Text1.place(relx=0.117, rely=0.069, relheight=0.153, relwidth=0.707)
        self.Text1.configure(background="white", font="TkTextFont", foreground="black",
                             highlightbackground="#d9d9d9", highlightcolor="black",
                             insertbackground="black", selectbackground="#c4c4c4",
                             selectforeground="black", width=424, wrap='word')

        self.Button1 = tk.Button(top, command=select_video_file)
        self.Button1.place(relx=0.848, rely=0.069, height=22, width=80)
        self.Button1.configure(activebackground="#ececec", activeforeground="#000000",
                               background="#d9d9d9", disabledforeground="#a3a3a3",
                               foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", pady="0", text='读取视频')

        self.Text2 = tk.Text(top)
        self.Text2.place(relx=0.117, rely=0.347, relheight=0.153, relwidth=0.707)
        self.Text2.configure(background="white", font="TkTextFont", foreground="black",
                             highlightbackground="#d9d9d9", highlightcolor="black",
                             insertbackground="black", selectbackground="#c4c4c4",
                             selectforeground="black", width=424, wrap='word')

        self.Button2 = tk.Button(top, command=select_audio_file)
        self.Button2.place(relx=0.848, rely=0.347, height=22, width=80)
        self.Button2.configure(activebackground="#ececec", activeforeground="#000000",
                               background="#d9d9d9", disabledforeground="#a3a3a3",
                               foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", pady="0", text='选择音频')

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.033, rely=0.069, height=23, width=38)
        self.Label1.configure(background="#d9d9d9", disabledforeground="#a3a3a3",
                              foreground="#000000", text='视频')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.033, rely=0.347, height=23, width=42)
        self.Label2.configure(background="#d9d9d9", disabledforeground="#a3a3a3",
                              foreground="#000000", text='音频')

        self.Button3 = tk.Button(top, command=merge_video_audio)
        self.Button3.place(relx=0.117, rely=0.625, height=28, width=519)
        self.Button3.configure(activebackground="#ececec", activeforeground="#000000",
                               background="#d9d9d9", disabledforeground="#a3a3a3",
                               foreground="#000000", highlightbackground="#d9d9d9",
                               highlightcolor="black", pady="0", text='合并视频和音频')


if __name__ == '__main__':
    vp_start_gui()