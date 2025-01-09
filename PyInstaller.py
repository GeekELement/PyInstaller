import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QLabel
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyInstaller")
        # 设置窗口固定宽度
        self.setFixedWidth(400)

        # 中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 总布局
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # 选择脚本部分
        self.select_layout = QHBoxLayout()
        self.main_layout.addLayout(self.select_layout)

        # 添加伸缩空间让按钮居中
        self.select_layout.addStretch()
        self.select_button = QPushButton("选择 Python 脚本路径")
        self.select_button.setFixedWidth(380)
        self.select_button.clicked.connect(self.select_script)
        self.select_layout.addWidget(self.select_button)
        self.select_layout.addStretch()

        # 开始打包按钮
        self.start_button = QPushButton("开始打包")
        self.select_button.setFixedWidth(380)
        self.start_button.clicked.connect(self.start_packaging)
        self.main_layout.addWidget(self.start_button)
        self.start_button.setEnabled(False)

        # 作者署名
        self.author_label = QLabel("作者：耑木菌")
        self.author_label.setAlignment(Qt.AlignRight)
        self.author_label.setStyleSheet("color: black; font-size: 12px;")
        self.main_layout.addWidget(self.author_label)

        # 调整布局间距
        self.main_layout.setSpacing(10)
        self.main_layout.addStretch(1)

    def select_script(self):
        # 打开文件选择对话框，选择 Python 脚本
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 Python 脚本", "", "Python 脚本 (*.py);;所有文件 (*.*)"
        )
        if file_path:
            self.start_button.setEnabled(True)
            self.script_path = file_path
        else:
            self.start_button.setEnabled(False)

    def start_packaging(self):
        # 检查是否选择了脚本
        if not hasattr(self, 'script_path') or not self.script_path:
            QMessageBox.warning(self, "错误", "请选择一个 Python 脚本。")
            return

        # 获取脚本的绝对路径
        script_abs_path = os.path.abspath(self.script_path)

        # 获取桌面路径
        desktop_path = os.path.expanduser('~\\Desktop')

        # 确保桌面路径存在
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)

        # PyInstaller 命令
        command = [
            'pyinstaller',
            '--onefile',
            f'--distpath={desktop_path}',
            script_abs_path
        ]

        try:
            # 运行 PyInstaller
            subprocess.run(command, check=True)
            QMessageBox.information(self, "成功", "打包完成！")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "错误", f"打包失败：{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())