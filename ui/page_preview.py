# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'page_preview.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_page_preview(object):
    def setupUi(self, page_preview):
        page_preview.setObjectName("page_preview")
        page_preview.resize(180, 56)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(page_preview.sizePolicy().hasHeightForWidth())
        page_preview.setSizePolicy(sizePolicy)
        page_preview.setMaximumSize(QtCore.QSize(180, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(page_preview)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.img_label = QtWidgets.QLabel(page_preview)
        self.img_label.setAlignment(QtCore.Qt.AlignCenter)
        self.img_label.setObjectName("img_label")
        self.verticalLayout.addWidget(self.img_label)
        self.text_label = QtWidgets.QLabel(page_preview)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setObjectName("text_label")
        self.verticalLayout.addWidget(self.text_label)

        self.retranslateUi(page_preview)
        QtCore.QMetaObject.connectSlotsByName(page_preview)

    def retranslateUi(self, page_preview):
        _translate = QtCore.QCoreApplication.translate
        page_preview.setWindowTitle(_translate("page_preview", "Frame"))
        self.img_label.setText(_translate("page_preview", "img"))
        self.text_label.setText(_translate("page_preview", "page"))
