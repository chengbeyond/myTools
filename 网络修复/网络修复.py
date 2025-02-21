import sys
import os
import winreg
import socket
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMutex
from PyQt5.QtGui import QFont, QColor, QPalette


# 工作线程类（保持不变）
class Worker(QThread):
    status_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.is_cancelled = False
        self.mutex = QMutex()

    def run(self):
        if self.task == 'disable_proxy':
            self.disable_proxy()
        elif self.task == 'test_network':
            self.test_network()
        if not self.is_cancelled:
            self.finished_signal.emit()

    def cancel(self):
        self.mutex.lock()
        self.is_cancelled = True
        self.mutex.unlock()

    def disable_proxy(self):
        try:
            self.status_signal.emit("正在准备关闭代理...")
            self.progress_signal.emit(10)
            time.sleep(0.1)
            if self.is_cancelled: return

            self.status_signal.emit("正在打开注册表...")
            self.progress_signal.emit(30)
            reg_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                0,
                winreg.KEY_WRITE
            )
            if self.is_cancelled:
                winreg.CloseKey(reg_key)
                return

            self.status_signal.emit("正在修改代理设置...")
            self.progress_signal.emit(60)
            winreg.SetValueEx(reg_key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            if self.is_cancelled:
                winreg.CloseKey(reg_key)
                return

            self.status_signal.emit("正在保存设置...")
            self.progress_signal.emit(90)
            winreg.CloseKey(reg_key)
            if not self.is_cancelled:
                self.status_signal.emit("代理已关闭")
                self.progress_signal.emit(100)
        except Exception as e:
            self.status_signal.emit(f"关闭代理错误: {str(e)}")
            self.progress_signal.emit(0)

    def test_network(self):
        try:
            self.status_signal.emit("正在初始化网络测试...")
            self.progress_signal.emit(10)
            time.sleep(0.1)
            if self.is_cancelled: return

            self.status_signal.emit("正在创建连接...")
            self.progress_signal.emit(30)
            socket.setdefaulttimeout(5)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.is_cancelled:
                sock.close()
                return

            self.status_signal.emit("正在尝试连接服务器...")
            self.progress_signal.emit(60)
            result = sock.connect_ex(('8.8.8.8', 53))
            if self.is_cancelled:
                sock.close()
                return

            self.status_signal.emit("正在清理资源...")
            self.progress_signal.emit(90)
            sock.close()
            if not self.is_cancelled:
                self.progress_signal.emit(100)
                if result == 0:
                    self.status_signal.emit("网络连接正常！")
                else:
                    self.status_signal.emit("网络连接失败！")
        except Exception as e:
            self.status_signal.emit(f"网络测试错误: {str(e)}")
            self.progress_signal.emit(0)


class ProxyNetworkTool(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.initUI()

    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('代理与网络工具')
        self.setFixedSize(350, 300)  # 固定窗口大小

        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(15)  # 控件间距

        # 创建控件
        self.proxy_button = QPushButton('关闭代理并测试', self)
        self.test_button = QPushButton('仅测试网络', self)
        self.cancel_button = QPushButton('取消任务', self)
        self.status_label = QLabel('点击按钮进行操作', self)
        self.progress_bar = QProgressBar(self)

        # 设置字体
        font = QFont('Arial', 10)
        self.proxy_button.setFont(font)
        self.test_button.setFont(font)
        self.cancel_button.setFont(font)
        self.status_label.setFont(font)

        # 美化样式
        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """
        self.proxy_button.setStyleSheet(button_style)
        self.test_button.setStyleSheet(button_style)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #333333; padding: 5px;")

        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)

        # 添加到布局
        layout.addWidget(self.proxy_button)
        layout.addWidget(self.test_button)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addStretch()

        self.setLayout(layout)
        self.cancel_button.setEnabled(False)

        # 连接信号
        self.proxy_button.clicked.connect(self.disable_proxy_and_test)
        self.test_button.clicked.connect(self.test_network)
        self.cancel_button.clicked.connect(self.cancel_task)

        # 设置窗口居中
        self.center()

    def center(self):
        # 获取屏幕几何信息并居中窗口
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)

    def update_status(self, text):
        self.status_label.setText(text)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def task_finished(self):
        self.proxy_button.setEnabled(True)
        self.test_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.worker = None

    def start_task(self, task):
        self.proxy_button.setEnabled(False)
        self.test_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setValue(0)

        self.worker = Worker(task)
        self.worker.status_signal.connect(self.update_status)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.task_finished)
        self.worker.start()

    def test_network(self):
        self.start_task('test_network')

    def disable_proxy_and_test(self):
        self.worker = Worker('disable_proxy')
        self.worker.status_signal.connect(self.on_proxy_finished)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_proxy_task_finished)
        self.proxy_button.setEnabled(False)
        self.test_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.worker.start()

    def on_proxy_finished(self, status):
        self.status_label.setText(status)

    def on_proxy_task_finished(self):
        if "已关闭" in self.status_label.text() and self.worker and not self.worker.is_cancelled:
            self.start_task('test_network')
        else:
            self.task_finished()

    def cancel_task(self):
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.status_label.setText("任务已取消")
            self.progress_bar.setValue(0)
            self.worker.wait()
            self.task_finished()


def run_as_admin():
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


if __name__ == '__main__':
    run_as_admin()
    app = QApplication(sys.argv)

    # 设置全局样式
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 245, 245))
    app.setPalette(palette)

    window = ProxyNetworkTool()
    window.show()
    sys.exit(app.exec_())