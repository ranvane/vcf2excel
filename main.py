import sys
import os
import re
import vobject
import xlsxwriter

from PySide6.QtWidgets import (
    QApplication, QWidget, QFileDialog, QMessageBox,
    QTableWidgetItem,QAbstractItemView, QHeaderView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from vcf_to_excel_ui import Ui_VCFtoExcelApp  # 你生成的UI类

class VCFtoExcelApp(QWidget, Ui_VCFtoExcelApp):
    """
    VCF到Excel转换器应用程序主类
    
    该类继承自QWidget和Ui_VCFtoExcelApp，实现了图形界面和功能逻辑
    """
    def __init__(self):
        """
        初始化VCFtoExcelApp实例
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("icons/icon.png"))

        # 初始化联系人数据
        self.contacts = []
        self.filtered_contacts = []

        # 信号连接
        self.select_button.clicked.connect(self.select_vcf_file)
        self.search_bar.textChanged.connect(self.filter_contacts)
        self.convert_button.clicked.connect(self.convert_to_excel)

        # 初始化表格
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.max_tel_count = 0
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()

    def select_vcf_file(self):
        """
        处理选择VCF文件的操作
        
        打开文件选择对话框，让用户选择VCF文件，并解析该文件中的联系人信息
        """
        home = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "选择VCF文件", home, "VCF文件 (*.vcf);;所有文件 (*)")
        if file_path:
            try:
                self.contacts = self.parse_vcf_safe(file_path)
                self.filtered_contacts = self.contacts.copy()
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
        刷新显示联系人信息的表格
        
        根据当前过滤后的联系人列表更新表格的列数和内容
        """
        # 计算最大电话号码数量以确定列数
        self.max_tel_count = max(
            (len(c.get("电话", "").split(",")) for c in self.filtered_contacts),
            default=1
        )
        column_count = 1 + self.max_tel_count  # 姓名 + 电话列数
        self.table.setColumnCount(column_count)

        # 设置表头
        headers = ["姓名"] + [f"电话{i+1}" for i in range(self.max_tel_count)]
        self.table.setHorizontalHeaderLabels(headers)

        # 填充表格数据
        self.table.setRowCount(len(self.filtered_contacts))
        for row, contact in enumerate(self.filtered_contacts):
            # 设置姓名
            name_item = QTableWidgetItem(contact.get("姓名", ""))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, name_item)

            # 设置电话号码
            tels = [t.strip() for t in contact.get("电话", "").split(",")]
            for i, tel in enumerate(tels):
                tel_item = QTableWidgetItem(tel)
                tel_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table.setItem(row, i + 1, tel_item)

        self.table.resizeColumnsToContents()


    def filter_contacts(self, text):
        """
        根据输入文本过滤联系人
        
        Args:
            text (str): 用于过滤联系人的搜索文本
        """
        text = text.strip().lower()
        self.filtered_contacts = [c for c in self.contacts if text in c.get("姓名", "").lower()]
        self.refresh_table()

    def convert_to_excel(self):
        """
        将联系人信息导出为Excel文件
        
        打开文件保存对话框，将当前显示的联系人信息保存为Excel格式文件
        """
        # 检查是否有联系人需要导出
        if not self.filtered_contacts:
            QMessageBox.information(self, "提示", "没有联系人可导出。")
            return
            
        # 获取保存路径
        save_path, _ = QFileDialog.getSaveFileName(self, "保存为Excel", "", "Excel 文件 (*.xlsx)")
        if not save_path:
            return
            
        # 导出到Excel
        try:
            workbook = xlsxwriter.Workbook(save_path)
            worksheet = workbook.add_worksheet("联系人")

            # 计算最大电话数量并设置表头
            max_tel_count = max(len(c.get("电话", "").split(",")) for c in self.filtered_contacts)
            header = ["姓名"] + [f"电话{i+1}" for i in range(max_tel_count)]
            for col, title in enumerate(header):
                worksheet.write(0, col, title)

            # 写入联系人数据
            for row, contact in enumerate(self.filtered_contacts, start=1):
                worksheet.write(row, 0, contact.get("姓名", ""))
                tels = [t.strip() for t in contact.get("电话", "").split(",")]
                for col, tel in enumerate(tels, start=1):
                    worksheet.write(row, col, tel)

            workbook.close()
            QMessageBox.information(self, "完成", f"联系人已成功导出到:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出Excel失败: {e}")

    def parse_vcf_safe(self, file_path):
        """
        安全地解析VCF文件
        
        Args:
            file_path (str): VCF文件的路径
            
        Returns:
            list: 包含联系人信息的字典列表，每个字典包含姓名和电话字段
            
        Raises:
            RuntimeError: 当vCard解析失败时抛出异常
        """
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            
        # 清理数据，移除换行符和照片数据
        data = re.sub(r'=\r?\n', '', data)
        data = re.sub(r'PHOTO;[^:]*:.*?(?=\n[A-Z]|$)', '', data, flags=re.DOTALL)
        
        # 解析vCard
        try:
            vcard_list = list(vobject.readComponents(data))
        except Exception as e:
            raise RuntimeError(f"vCard解析失败: {e}")

        # 提取联系人信息
        contacts = []
        for vcard in vcard_list:
            name = vcard.fn.value if hasattr(vcard, 'fn') else ''
            tels = [tel.value for tel in getattr(vcard, 'tel_list', [])]
            contacts.append({
                '姓名': name,
                '电话': ', '.join(tels)
            })
        return contacts


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VCFtoExcelApp()
    window.show()
    sys.exit(app.exec())
