import sys

from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QPushButton, QWidget

from PyQt5 import uic

app = QApplication(sys.argv)

# 创建主窗口
window = QWidget()

src = "D:\py project\炫压抑管理系统\code\Home.ui"

ui = uic.loadUi(src)
ui.show()
app.exec_()