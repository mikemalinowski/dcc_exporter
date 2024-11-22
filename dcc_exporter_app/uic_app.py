# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(813, 832)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(u"main_layout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.add_button = QPushButton(Form)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setMinimumSize(QSize(30, 30))
        self.add_button.setMaximumSize(QSize(30, 30))
        self.add_button.setStyleSheet(u"font: 16pt \"Segoe UI\";")

        self.verticalLayout.addWidget(self.add_button)

        self.remove_button = QPushButton(Form)
        self.remove_button.setObjectName(u"remove_button")
        self.remove_button.setMinimumSize(QSize(30, 30))
        self.remove_button.setMaximumSize(QSize(30, 30))

        self.verticalLayout.addWidget(self.remove_button)

        self.settings_button = QPushButton(Form)
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setMinimumSize(QSize(30, 30))
        self.settings_button.setMaximumSize(QSize(30, 30))
        self.settings_button.setStyleSheet(u"font: 9pt \"Wingdings\";")

        self.verticalLayout.addWidget(self.settings_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.export_list = QListWidget(Form)
        self.export_list.setObjectName(u"export_list")
        self.export_list.setAlternatingRowColors(True)
        self.export_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.export_list.setIconSize(QSize(32, 32))
        self.export_list.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.export_list)

        self.export_button = QPushButton(Form)
        self.export_button.setObjectName(u"export_button")

        self.verticalLayout_2.addWidget(self.export_button)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.options_layout = QVBoxLayout()
        self.options_layout.setObjectName(u"options_layout")

        self.horizontalLayout.addLayout(self.options_layout)

        self.horizontalLayout.setStretch(2, 1)

        self.main_layout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 6pt \"MS Shell Dlg 2\";")

        self.horizontalLayout_2.addWidget(self.label)

        self.version_label = QLabel(Form)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setStyleSheet(u"font: 6pt \"MS Shell Dlg 2\";")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.version_label)


        self.main_layout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addLayout(self.main_layout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.add_button.setText(QCoreApplication.translate("Form", u"+", None))
        self.remove_button.setText(QCoreApplication.translate("Form", u"-", None))
        self.settings_button.setText(QCoreApplication.translate("Form", u"R", None))
        self.export_button.setText(QCoreApplication.translate("Form", u"Export", None))
        self.label.setText(QCoreApplication.translate("Form", u"Open Source DCC Export Framework (xstack)", None))
        self.version_label.setText(QCoreApplication.translate("Form", u"v0.0.0", None))
    # retranslateUi

