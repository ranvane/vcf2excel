"""
此模块实现了一个基于 PySide6 的 GUI 应用程序，用于将 VCF 通讯录文件转换为 Excel 表格。
用户可以选择 VCF 文件，搜索联系人，并将筛选后的联系人导出为 Excel 文件。
"""
import os
import re
import vobject
import xlsxwriter
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt


class VCFtoExcelApp(QWidget):
    """
    该类实现了一个图形用户界面应用程序，用于将 VCF 文件转换为 Excel 文件。
    支持选择 VCF 文件、搜索联系人以及导出联系人信息到 Excel 表格。
    """
    def __init__(self):
        """
        初始化 VCFtoExcelApp 类的实例。
        设置窗口标题，初始化联系人列表和筛选后的联系人列表，
        并构建用户界面布局。
        """
        super().__init__()
        self.setWindowTitle("VCF 转 Excel 工具")
        # 存储所有解析后的联系人信息
        self.contacts = []
        # 存储筛选后的联系人信息
        self.filtered_contacts = []

        # 创建垂直布局
        layout = QVBoxLayout()
        # 创建水平布局
        hlayout = QHBoxLayout()
        # 定义按钮的样式表
        button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """
        # 定义输入框的样式表
        lineEdit_style = """
        QLineEdit {
        padding: 6px 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 14px;
        }
        QLineEdit:focus {
                border: 1px solid #4CAF50;
                outline: none;
            }
        """

        # 定义表格的样式表
        table_style = """
        QTableWidget {
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
            selection-background-color: #4CAF50;
            selection-color: white;
            background-color: white;
            alternate-background-color: #f9f9f9;
        }
        QHeaderView::section {
            background-color: #C8E6C9;
            color: #000000;
            padding: 4px;
            border: none;
            font-weight: bold;
        }
        """
        # 创建选择 VCF 文件的按钮
        self.select_button = QPushButton("选择VCF文件")
        self.select_button.setStyleSheet(button_style)
        # 连接按钮点击事件到选择 VCF 文件的方法
        self.select_button.clicked.connect(self.select_vcf_file)
        hlayout.addWidget(self.select_button)

        # 创建搜索联系人的输入框
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("搜索联系人姓名...")
        self.search_bar.setStyleSheet(lineEdit_style)
        # 连接输入框文本变化事件到筛选联系人的方法
        self.search_bar.textChanged.connect(self.filter_contacts)
        hlayout.addWidget(self.search_bar)

        # 创建转换为 Excel 的按钮
        self.convert_button = QPushButton("转换为Excel")
        self.convert_button.setStyleSheet(button_style)
        # 连接按钮点击事件到转换为 Excel 的方法
        self.convert_button.clicked.connect(self.convert_to_excel)
        hlayout.addWidget(self.convert_button)

        # 将水平布局添加到垂直布局中
        layout.addLayout(hlayout)

        # 创建提示标签
        self.label = QLabel("尚未选择VCF文件")
        layout.addWidget(self.label)

        # 创建表格用于显示联系人信息
        self.table = QTableWidget(0, 2)
        self.table.setStyleSheet(table_style)
        # 设置表格的列标题
        self.table.setHorizontalHeaderLabels(["姓名", "电话"])
        # 设置表格不可编辑
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # 设置表格选择行为为整行选择
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        # 设置表格选择模式为单选
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # 设置表格最后一列自动拉伸
        self.table.horizontalHeader().setStretchLastSection(True)
        # 隐藏表格垂直表头
        self.table.verticalHeader().setVisible(False)
        # 设置表格隔行变色
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        # 将窗口居中显示
        self.center_window()

        # 设置窗口的布局
        self.setLayout(layout)

    def center_window(self):
        """
        将窗口居中显示在屏幕上。
        """
        frame_gm = self.frameGeometry()
        screen = QApplication.primaryScreen()
        screen_center = screen.availableGeometry().center()
        frame_gm.moveCenter(screen_center)
        self.move(frame_gm.topLeft())

    def select_vcf_file(self):
        """
        打开文件选择对话框，让用户选择 VCF 文件。
        若选择成功，则解析文件并刷新表格显示联系人信息；
        若解析失败，则弹出错误提示框。
        """
        home = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择VCF文件", home, "VCF文件 (*.vcf);;所有文件 (*)"
        )
        if file_path:
            try:
                # 安全解析 VCF 文件
                self.contacts = self.parse_vcf_safe(file_path)
                self.filtered_contacts = self.contacts.copy()
                # 刷新表格显示联系人信息
                self.refresh_table()
                self.label.setText(f"已选择文件: {os.path.basename(file_path)}（共 {len(self.contacts)} 个联系人）")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"解析VCF文件失败: {e}")
                self.contacts = []
                self.filtered_contacts = []
                self.refresh_table()
                self.label.setText("VCF文件解析失败")

    def refresh_table(self):
        """
        刷新表格内容，根据筛选后的联系人信息更新表格显示。
        """
        self.table.clearContents()
        self.table.setRowCount(len(self.filtered_contacts))

        for row, contact in enumerate(self.filtered_contacts):
            # 创建姓名表格项
            name_item = QTableWidgetItem(contact.get('姓名', ''))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, name_item)

            # 处理电话信息，多行显示
            tels = contact.get('电话', '').split(',')
            tel_text = "\n".join([tel.strip() for tel in tels])
            # 创建电话表格项
            tel_item = QTableWidgetItem(tel_text)
            tel_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 1, tel_item)

        # 自动调整列宽
        self.table.resizeColumnsToContents()

    def filter_contacts(self, text):
        """
        根据输入的文本筛选联系人，更新筛选后的联系人列表并刷新表格。

        Args:
            text (str): 用于筛选联系人姓名的文本。
        """
        text = text.strip().lower()
        self.filtered_contacts = [
            c for c in self.contacts if text in c.get('姓名', '').lower()
        ]
        self.refresh_table()

    def convert_to_excel(self):
        """
        将筛选后的联系人信息导出为 Excel 文件。
        若没有可导出的联系人，弹出提示框；
        若导出失败，弹出错误提示框。
        """
        if not self.filtered_contacts:
            QMessageBox.information(self, "提示", "没有联系人可导出。")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "保存为Excel", "", "Excel 文件 (*.xlsx)")
        if not save_path:
            return

        try:
            # 创建 Excel 工作簿
            workbook = xlsxwriter.Workbook(save_path)
            # 添加工作表
            worksheet = workbook.add_worksheet("联系人")

            # 计算最大电话列数
            max_tel_count = max(len(contact.get('电话', '').split(',')) for contact in self.filtered_contacts)
            header = ["姓名"] + [f"电话{i+1}" for i in range(max_tel_count)]
            for col, title in enumerate(header):
                worksheet.write(0, col, title)

            for row, contact in enumerate(self.filtered_contacts, start=1):
                worksheet.write(row, 0, contact.get('姓名', ''))
                tels = [tel.strip() for tel in contact.get('电话', '').split(',')]
                for col, tel in enumerate(tels, start=1):
                    worksheet.write(row, col, tel)

            # 关闭工作簿
            workbook.close()
            QMessageBox.information(self, "完成", f"联系人已成功导出到:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出Excel失败: {e}")

    def parse_vcf_safe(self, file_path):
        """
        安全地解析 VCF 文件，处理换行和照片字段。

        Args:
            file_path (str): VCF 文件的路径。

        Returns:
            list: 解析后的联系人信息列表，每个联系人是一个字典。
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()

        # 处理换行符
        data = re.sub(r'=\r?\n', '', data)
        # 移除照片字段
        data = self.remove_photo_field(data)

        try:
            # 解析 VCF 文件
            vcard_list = list(vobject.readComponents(data))
        except Exception as e:
            raise RuntimeError(f"vCard解析失败: {e}")

        contacts = []
        for vcard in vcard_list:
            name = vcard.fn.value if hasattr(vcard, 'fn') else ''
            tels = []
            if hasattr(vcard, 'tel_list'):
                for tel in vcard.tel_list:
                    tels.append(tel.value)
            contacts.append({
                '姓名': name,
                '电话': ', '.join(tels)
            })

        return contacts

    def remove_photo_field(self, data):
        """
        从 VCF 文件内容中移除照片字段。

        Args:
            data (str): VCF 文件的内容。

        Returns:
            str: 移除照片字段后的 VCF 文件内容。
        """
        return re.sub(r'PHOTO;[^:]*:.*?(?=\n[A-Z]|$)', '', data, flags=re.DOTALL)


if __name__ == "__main__":
    import sys
    # 创建应用程序实例
    app = QApplication(sys.argv)
    # 创建窗口实例
    window = VCFtoExcelApp()
    window.resize(700, 500)
    window.show()
    sys.exit(app.exec())
