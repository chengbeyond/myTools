import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
from bs4 import BeautifulSoup

class Worker(QThread):
    finished = pyqtSignal(str)  # 自定义信号传递结果

    def __init__(self, input_text):
        super().__init__()
        self.input_text = input_text

    def run(self):
        try:
            url = f"https://www.javbus.com/{self.input_text}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }

            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                container_div = soup.find('div', class_='container')
                if container_div:
                    star_name_divs = container_div.find_all('div', class_='star-name')
                    if star_name_divs:
                        result = ""
                        for div in star_name_divs:
                            result += f"{div.get_text(strip=True)}\n"
                    else:
                        result = "没有找到类名为star-ame的<div>"
                else:
                    result = "没有找到类名为container的<div>"
            else:
                result = f"请求失败，可能没有这个番号，状态码: {response.status_code}"

        except Exception as e:
            result = f"发生错误: {str(e)}"

        self.finished.emit(result)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("番号查询女优")
        self.init_ui()
        self.center()

    def init_ui(self):
        layout = QVBoxLayout(self)

        input_label = QLabel("请输入番号:")
        layout.addWidget(input_label)

        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(30)
        layout.addWidget(self.input_field)

        search_button = QPushButton("查询女优名")
        search_button.clicked.connect(self.search_name)
        search_button.setFixedHeight(35)
        layout.addWidget(search_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

    def center(self):
        qr = self.frameGeometry()
        cp = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def search_name(self):
        name = self.input_field.text().strip()
        if not name:
            QMessageBox.information(self, "提示", "请输入番号！")
            return

        # 清空结果
        self.result_text.clear()

        # 启动线程进行查询
        self.worker = Worker(name)
        self.worker.finished.connect(self.update_result)
        self.worker.start()

    def update_result(self, result):
        self.result_text.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
