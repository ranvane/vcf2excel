# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vcf_to_excel.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_VCFtoExcelApp(object):
    def setupUi(self, VCFtoExcelApp):
        if not VCFtoExcelApp.objectName():
            VCFtoExcelApp.setObjectName(u"VCFtoExcelApp")
        VCFtoExcelApp.resize(800, 600)
        VCFtoExcelApp.setMinimumSize(QSize(800, 600))
        VCFtoExcelApp.setMaximumSize(QSize(800, 600))
        self.verticalLayout = QVBoxLayout(VCFtoExcelApp)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.select_button = QPushButton(VCFtoExcelApp)
        self.select_button.setObjectName(u"select_button")
        self.select_button.setStyleSheet(u"QPushButton {\n"
" background-color: #4CAF50;\n"
" color: white;\n"
" padding: 6px 12px;\n"
" border: none;\n"
" border-radius: 4px;\n"
"}\n"
"QPushButton:hover {\n"
" background-color: #45a049;\n"
"}")

        self.horizontalLayout.addWidget(self.select_button)

        self.search_bar = QLineEdit(VCFtoExcelApp)
        self.search_bar.setObjectName(u"search_bar")
        self.search_bar.setStyleSheet(u"QLineEdit {\n"
" padding: 6px 12px;\n"
" border: 1px solid #ccc;\n"
" border-radius: 4px;\n"
" font-size: 14px;\n"
"}\n"
"QLineEdit:focus {\n"
" border: 1px solid #4CAF50;\n"
" outline: none;\n"
"}")

        self.horizontalLayout.addWidget(self.search_bar)

        self.convert_button = QPushButton(VCFtoExcelApp)
        self.convert_button.setObjectName(u"convert_button")
        self.convert_button.setStyleSheet(u"QPushButton {\n"
" background-color: #4CAF50;\n"
" color: white;\n"
" padding: 6px 12px;\n"
" border: none;\n"
" border-radius: 4px;\n"
"}\n"
"QPushButton:hover {\n"
" background-color: #45a049;\n"
"}")

        self.horizontalLayout.addWidget(self.convert_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(VCFtoExcelApp)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.table = QTableWidget(VCFtoExcelApp)
        if (self.table.columnCount() < 2):
            self.table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table.setObjectName(u"table")
        self.table.setStyleSheet(u"QTableWidget {\n"
" border: 1px solid #ccc;\n"
" border-radius: 4px;\n"
" font-size: 14px;\n"
" selection-background-color: #4CAF50;\n"
" selection-color: white;\n"
" background-color: white;\n"
" alternate-background-color: #f9f9f9;\n"
"}\n"
"QHeaderView::section {\n"
" background-color: #C8E6C9;\n"
" color: #000000;\n"
" padding: 4px;\n"
" border: none;\n"
" font-weight: bold;\n"
"}")
        self.table.setRowCount(0)
        self.table.setColumnCount(2)

        self.verticalLayout.addWidget(self.table)


        self.retranslateUi(VCFtoExcelApp)

        QMetaObject.connectSlotsByName(VCFtoExcelApp)
    # setupUi

    def retranslateUi(self, VCFtoExcelApp):
        VCFtoExcelApp.setWindowTitle(QCoreApplication.translate("VCFtoExcelApp", u"VCF \u8f6c Excel \u5de5\u5177", None))
        self.select_button.setText(QCoreApplication.translate("VCFtoExcelApp", u"\u9009\u62e9VCF\u6587\u4ef6", None))
        self.search_bar.setPlaceholderText(QCoreApplication.translate("VCFtoExcelApp", u"\u641c\u7d22\u8054\u7cfb\u4eba\u59d3\u540d...", None))
        self.convert_button.setText(QCoreApplication.translate("VCFtoExcelApp", u"\u8f6c\u6362\u4e3aExcel", None))
        self.label.setText(QCoreApplication.translate("VCFtoExcelApp", u"\u5c1a\u672a\u9009\u62e9VCF\u6587\u4ef6", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("VCFtoExcelApp", u"\u59d3\u540d", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("VCFtoExcelApp", u"\u7535\u8bdd", None));
    # retranslateUi

