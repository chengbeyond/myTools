from tkinter import filedialog, messagebox
import threading
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import VideoSplitting_support
import subprocess
import os

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
    top = Toplevel1 (root)
    VideoSplitting_support.init(root, top)
    center_window(root, 600, 233)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    VideoSplitting_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("600x233")
        top.title("Video Splitting")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.033, rely=0.086, height=23, width=37)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''路径''')

        self.Text1 = tk.Text(top)
        self.Text1.place(relx=0.133, rely=0.086, relheight=0.094, relwidth=0.823)
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

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.133, rely=0.258, height=28, width=75)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''读取文件''')
        self.Button1.config(command=self.load_file)

        self.Text2 = tk.Text(top)
        self.Text2.place(relx=0.133, rely=0.515, relheight=0.094, relwidth=0.157)
        self.Text2.configure(background="white")
        self.Text2.configure(font="TkTextFont")
        self.Text2.configure(foreground="black")
        self.Text2.configure(highlightbackground="#d9d9d9")
        self.Text2.configure(highlightcolor="black")
        self.Text2.configure(insertbackground="black")
        self.Text2.configure(selectbackground="#c4c4c4")
        self.Text2.configure(selectforeground="black")
        self.Text2.insert(tk.END, '00:00:00')  # Set default time
        self.Text2.configure(width=94)
        self.Text2.configure(wrap='word')

        self.Text3 = tk.Text(top)
        self.Text3.place(relx=0.4, rely=0.515, relheight=0.094, relwidth=0.157)
        self.Text3.configure(background="white")
        self.Text3.configure(font="TkTextFont")
        self.Text3.configure(foreground="black")
        self.Text3.configure(highlightbackground="#d9d9d9")
        self.Text3.configure(highlightcolor="black")
        self.Text3.configure(insertbackground="black")
        self.Text3.configure(selectbackground="#c4c4c4")
        self.Text3.configure(selectforeground="black")
        self.Text3.insert(tk.END, '00:00:00')  # Set default time
        self.Text3.configure(width=94)
        self.Text3.configure(wrap='word')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.033, rely=0.515, height=23, width=37)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''开始''')

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.317, rely=0.515, height=23, width=37)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''结束''')

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.133, rely=0.73, height=28, width=75)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''开始分割''')
        self.Button2.config(command=self.split_media)

    def load_file(self):
        '''Load file and display its path in Text1'''
        filename = filedialog.askopenfilename()
        self.Text1.delete(1.0, tk.END)
        self.Text1.insert(tk.END, filename)

    def split_media(self):
        '''Split media based on start and end times'''
        self.Button2.config(state=tk.DISABLED, text='分割中')  # 设置按钮为不可点击并更改文本
        thread = threading.Thread(target=self._split_media)
        thread.start()

    def _split_media(self):
        '''Internal method to handle the actual media splitting process.'''
        file_path = self.Text1.get(1.0, tk.END).strip()
        start_time = self.Text2.get(1.0, tk.END).strip()
        end_time = self.Text3.get(1.0, tk.END).strip()
        if file_path and start_time and end_time:
            extension = os.path.splitext(file_path)[1].lower()
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_dir = os.path.dirname(file_path)
            output_file = os.path.join(output_dir, f"{base_name}_split{extension}")
            command = f"ffmpeg -i {file_path} -ss {start_time} -to {end_time} -c copy -avoid_negative_ts make_zero {output_file}"
            print(command)
            result = subprocess.run(command, shell=True, capture_output=True)
            if result.returncode == 0:
                self.Button2.config(state=tk.NORMAL, text='开始分割')  # 恢复按钮状态
                messagebox.showinfo("Media Splitting", "Media has been split successfully!")
            else:
                self.Button2.config(state=tk.NORMAL, text='开始分割')  # 恢复按钮状态
                messagebox.showerror("Error",
                                     f"An error occurred during the split operation.\n{result.stderr.decode('utf-8')}")
        else:
            self.Button2.config(state=tk.NORMAL, text='开始分割')  # 恢复按钮状态
            messagebox.showerror("Error", "Please fill in all fields correctly.")


if __name__ == '__main__':
    vp_start_gui()