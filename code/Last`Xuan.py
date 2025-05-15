import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt5 import uic

# 数据库操作函数
def open_db():
    """打开数据库连接"""
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="03516168850xu",  # 修改为你的密码
        db="xuanyayi",
        charset='utf8mb4'
    )


def add_data(name, age, tel, voice, comment):
    """添加数据"""
    with open_db() as db:
        sql = "INSERT INTO wamom (name, age, tel, voice, comment) VALUES (%s, %s, %s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(sql, (name, age, tel, voice, comment))
        db.commit()


def delete_data(tel):
    """删除数据"""
    with open_db() as db:
        sql = "DELETE FROM wamom WHERE tel = %s"
        cursor = db.cursor()
        cursor.execute(sql, (tel,))
        db.commit()


def get_all_data(start=0):
    """获取全部数据"""

    with open_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM wamom limit %s,15", (start,))
        return cursor.fetchall()


# 主窗口
class MainWindow(QMainWindow):
    page_start = 0
    def __init__(self):
        super().__init__()
        # 加载UI文件（修改为你的Home.ui路径）
        uic.loadUi("D:/py project/炫压抑管理系统/code/Home.ui", self)

        # 初始化界面
        #self.tableWidget.setHorizontalHeaderLabels(["姓名", "年龄", "电话", "声音", "备注"])
        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 120)

        # 定义信号
        self.addBtn = self.pushButton_2
        self.delBtn = self.pushButton
        self.nextpageBtn = self.pushButton_4
        self.lastpageBtn = self.pushButton_5
        self.pageNum = self.lineEdit



        # 绑定槽函数
        self.addBtn.clicked.connect(self.show_add_dialog)
        self.delBtn.clicked.connect(self.delete_record)
        self.nextpageBtn.clicked.connect(self.next_page)
        self.lastpageBtn.clicked.connect(self.last_page)
        self.pageNum.returnPressed.connect(self.skip_page)
        # 初始加载数据
        self.load_data()

    def load_data(self, start= 0):

        """加载数据到表格"""
        try:
            data = get_all_data(start)
            # 显示行数
            self.tableWidget.setRowCount(10)
            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.clearContents()
            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.tableWidget.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据失败: {str(e)}")

    def show_add_dialog(self):
        """显示添加对话框"""
        dialog = AddDialog(self)
        if dialog.exec_():
            self.load_data()  # 对话框关闭后刷新数据

    def delete_record(self):
        """删除记录"""
        tel, ok = QInputDialog.getText(self, "删除记录", "请输入要删除的电话号码:")
        if ok and tel:
            try:
                delete_data(tel)
                self.load_data()
                QMessageBox.information(self, "成功", "删除成功！")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {str(e)}")

    def next_page(self):
        if (MainWindow.page_start+10)<=len(get_all_data()):
            MainWindow.page_start = MainWindow.page_start + 10
            self.load_data(MainWindow.page_start)




    def last_page(self):
        if (MainWindow.page_start - 10)>=0 :
            MainWindow.page_start = MainWindow.page_start - 10
            self.load_data(MainWindow.page_start)



    def skip_page(self):
        try:
            num = int(self.pageNum.text())
            if (num>0 and len(get_all_data())//10+1>=num):
                self.load_data((num-1)*10)
            else:
                QMessageBox.warning(self, "警告", "数据不够多呢")
        except:
            QMessageBox.warning(self, "警告", "请填合法数字")

# 添加对话框
class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 加载UI文件（修改为你的Edit.ui路径）
        uic.loadUi("D:/py project/炫压抑管理系统/code/Edit.ui", self)

        # 绑定按钮事件
        self.OK.clicked.connect(self.submit_data)
        self.Cancel.clicked.connect(self.reject)

    def submit_data(self):
        """提交数据"""
        name = self.lineEdit_2.text().strip()
        age = self.lineEdit_3.text().strip()
        tel = self.lineEdit_4.text().strip()
        voice = self.lineEdit.text().strip()
        comment = self.textEdit.toPlainText().strip()

        # 输入验证
        if not all([name, age, tel]):
            QMessageBox.warning(self, "警告", "姓名、年龄、电话为必填项！")
            return

        try:
            add_data(name, age, tel, voice, comment)
            self.accept()  # 关闭对话框并返回成功
        except Exception as e:
            QMessageBox.critical(self, "错误", f"添加失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 检查数据库连接
    try:
        with open_db() as db:
            pass
    except Exception as e:
        QMessageBox.critical(None, "数据库错误", f"无法连接数据库: {str(e)}")
        sys.exit(1)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())