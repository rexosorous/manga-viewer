# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bookshelf_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_bookshelf_panel(object):
    def setupUi(self, bookshelf_panel):
        bookshelf_panel.setObjectName("bookshelf_panel")
        bookshelf_panel.resize(1600, 900)
        self.verticalLayout = QtWidgets.QVBoxLayout(bookshelf_panel)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(bookshelf_panel)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_bar = QtWidgets.QLineEdit(self.frame)
        self.search_bar.setObjectName("search_bar")
        self.horizontalLayout_2.addWidget(self.search_bar)
        self.search_button = QtWidgets.QPushButton(self.frame)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_2.addWidget(self.search_button)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.sort_by = QtWidgets.QComboBox(self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.sort_by.setPalette(palette)
        self.sort_by.setObjectName("sort_by")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.sort_by.addItem("")
        self.horizontalLayout_2.addWidget(self.sort_by)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.random_button = QtWidgets.QPushButton(self.frame)
        self.random_button.setObjectName("random_button")
        self.horizontalLayout_2.addWidget(self.random_button)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(bookshelf_panel)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.main_area = QtWidgets.QHBoxLayout(self.frame_2)
        self.main_area.setContentsMargins(-1, 0, -1, 0)
        self.main_area.setObjectName("main_area")
        self.bookshelf_scroll_area = QtWidgets.QScrollArea(self.frame_2)
        self.bookshelf_scroll_area.setFrameShape(QtWidgets.QFrame.Box)
        self.bookshelf_scroll_area.setFrameShadow(QtWidgets.QFrame.Plain)
        self.bookshelf_scroll_area.setWidgetResizable(True)
        self.bookshelf_scroll_area.setObjectName("bookshelf_scroll_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1578, 862))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.bookshelf_layout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.bookshelf_layout.setVerticalSpacing(50)
        self.bookshelf_layout.setObjectName("bookshelf_layout")
        self.bookshelf_scroll_area.setWidget(self.scrollAreaWidgetContents_2)
        self.main_area.addWidget(self.bookshelf_scroll_area)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(bookshelf_panel)
        QtCore.QMetaObject.connectSlotsByName(bookshelf_panel)

    def retranslateUi(self, bookshelf_panel):
        _translate = QtCore.QCoreApplication.translate
        bookshelf_panel.setWindowTitle(_translate("bookshelf_panel", "Frame"))
        self.search_button.setText(_translate("bookshelf_panel", "Search"))
        self.label.setText(_translate("bookshelf_panel", "Sort"))
        self.sort_by.setItemText(0, _translate("bookshelf_panel", "Title (A to Z)"))
        self.sort_by.setItemText(1, _translate("bookshelf_panel", "Title (Z to A)"))
        self.sort_by.setItemText(2, _translate("bookshelf_panel", "Rating (0 to 10)"))
        self.sort_by.setItemText(3, _translate("bookshelf_panel", "Rating (10 to 0)"))
        self.sort_by.setItemText(4, _translate("bookshelf_panel", "Pages (low to high)"))
        self.sort_by.setItemText(5, _translate("bookshelf_panel", "Pages (high to low)"))
        self.sort_by.setItemText(6, _translate("bookshelf_panel", "Date Added (old to new)"))
        self.sort_by.setItemText(7, _translate("bookshelf_panel", "Date Added (new to old)"))
        self.sort_by.setItemText(8, _translate("bookshelf_panel", "Randomly"))
        self.random_button.setText(_translate("bookshelf_panel", "Select Random"))
