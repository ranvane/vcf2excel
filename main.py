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
    def __init__(self):
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
        self.max_tel_count = max(
            (len(c.get("电话", "").split(",")) for c in self.filtered_contacts),
            default=1
        )
        column_count = 1 + self.max_tel_count  # 姓名 + 电话列数
        self.table.setColumnCount(column_count)

        headers = ["姓名"] + [f"电话{i+1}" for i in range(self.max_tel_count)]
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(self.filtered_contacts))
        for row, contact in enumerate(self.filtered_contacts):
            name_item = QTableWidgetItem(contact.get("姓名", ""))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, name_item)

            tels = [t.strip() for t in contact.get("电话", "").split(",")]
            for i, tel in enumerate(tels):
                tel_item = QTableWidgetItem(tel)
                tel_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table.setItem(row, i + 1, tel_item)

        self.table.resizeColumnsToContents()


    def filter_contacts(self, text):
        text = text.strip().lower()
        self.filtered_contacts = [c for c in self.contacts if text in c.get("姓名", "").lower()]
        self.refresh_table()

    def convert_to_excel(self):
        if not self.filtered_contacts:
            QMessageBox.information(self, "提示", "没有联系人可导出。")
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "保存为Excel", "", "Excel 文件 (*.xlsx)")
        if not save_path:
            return
        try:
            workbook = xlsxwriter.Workbook(save_path)
            worksheet = workbook.add_worksheet("联系人")

            max_tel_count = max(len(c.get("电话", "").split(",")) for c in self.filtered_contacts)
            header = ["姓名"] + [f"电话{i+1}" for i in range(max_tel_count)]
            for col, title in enumerate(header):
                worksheet.write(0, col, title)

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
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        data = re.sub(r'=\r?\n', '', data)
        data = re.sub(r'PHOTO;[^:]*:.*?(?=\n[A-Z]|$)', '', data, flags=re.DOTALL)
        try:
            vcard_list = list(vobject.readComponents(data))
        except Exception as e:
            raise RuntimeError(f"vCard解析失败: {e}")

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
