# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_search_panel(object):
    def setupUi(self, search_panel):
        search_panel.setObjectName("search_panel")
        search_panel.resize(351, 958)
        search_panel.setMaximumSize(QtCore.QSize(352, 16777215))
        search_panel.setFrameShape(QtWidgets.QFrame.Box)
        self.formLayout = QtWidgets.QFormLayout(search_panel)
        self.formLayout.setContentsMargins(-1, 0, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_14 = QtWidgets.QLabel(search_panel)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_14)
        self.frame_4 = QtWidgets.QFrame(search_panel)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.filter_prev_button = QtWidgets.QPushButton(self.frame_4)
        self.filter_prev_button.setMaximumSize(QtCore.QSize(50, 16777215))
        self.filter_prev_button.setObjectName("filter_prev_button")
        self.horizontalLayout_5.addWidget(self.filter_prev_button)
        self.filter_text = QtWidgets.QLabel(self.frame_4)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.filter_text.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.filter_text.setFont(font)
        self.filter_text.setAlignment(QtCore.Qt.AlignCenter)
        self.filter_text.setObjectName("filter_text")
        self.horizontalLayout_5.addWidget(self.filter_text)
        self.filter_next_button = QtWidgets.QPushButton(self.frame_4)
        self.filter_next_button.setMaximumSize(QtCore.QSize(50, 16777215))
        self.filter_next_button.setObjectName("filter_next_button")
        self.horizontalLayout_5.addWidget(self.filter_next_button)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.frame_4)
        self.label_15 = QtWidgets.QLabel(search_panel)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.title_text = QtWidgets.QLineEdit(search_panel)
        self.title_text.setObjectName("title_text")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.title_text)
        self.label_16 = QtWidgets.QLabel(search_panel)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.frame_19 = QtWidgets.QFrame(search_panel)
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_19)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.artists_text = QtWidgets.QLineEdit(self.frame_19)
        self.artists_text.setObjectName("artists_text")
        self.verticalLayout_11.addWidget(self.artists_text)
        self.artists_list = QtWidgets.QListWidget(self.frame_19)
        self.artists_list.setObjectName("artists_list")
        self.verticalLayout_11.addWidget(self.artists_list)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.frame_19)
        self.label_17 = QtWidgets.QLabel(search_panel)
        self.label_17.setObjectName("label_17")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.frame_10 = QtWidgets.QFrame(search_panel)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.series_text = QtWidgets.QLineEdit(self.frame_10)
        self.series_text.setObjectName("series_text")
        self.verticalLayout_10.addWidget(self.series_text)
        self.series_list = QtWidgets.QListWidget(self.frame_10)
        self.series_list.setObjectName("series_list")
        self.verticalLayout_10.addWidget(self.series_list)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.frame_10)
        self.label_18 = QtWidgets.QLabel(search_panel)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.order_number = QtWidgets.QSpinBox(search_panel)
        self.order_number.setObjectName("order_number")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.order_number)
        self.label_19 = QtWidgets.QLabel(search_panel)
        self.label_19.setObjectName("label_19")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.frame_7 = QtWidgets.QFrame(search_panel)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rating_number = QtWidgets.QSpinBox(self.frame_7)
        self.rating_number.setMaximum(10)
        self.rating_number.setObjectName("rating_number")
        self.horizontalLayout_3.addWidget(self.rating_number)
        self.rating_toggle = QtWidgets.QCheckBox(self.frame_7)
        self.rating_toggle.setChecked(True)
        self.rating_toggle.setObjectName("rating_toggle")
        self.horizontalLayout_3.addWidget(self.rating_toggle)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.frame_7)
        self.label = QtWidgets.QLabel(search_panel)
        self.label.setObjectName("label")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label)
        self.frame = QtWidgets.QFrame(search_panel)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pages_number_low = QtWidgets.QSpinBox(self.frame)
        self.pages_number_low.setObjectName("pages_number_low")
        self.horizontalLayout.addWidget(self.pages_number_low)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.pages_number_high = QtWidgets.QSpinBox(self.frame)
        self.pages_number_high.setObjectName("pages_number_high")
        self.horizontalLayout.addWidget(self.pages_number_high)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.frame)
        self.label_2 = QtWidgets.QLabel(search_panel)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.frame_2 = QtWidgets.QFrame(search_panel)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.date_low = QtWidgets.QDateTimeEdit(self.frame_2)
        self.date_low.setCalendarPopup(True)
        self.date_low.setObjectName("date_low")
        self.horizontalLayout_2.addWidget(self.date_low)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.date_high = QtWidgets.QDateTimeEdit(self.frame_2)
        self.date_high.setCalendarPopup(True)
        self.date_high.setObjectName("date_high")
        self.horizontalLayout_2.addWidget(self.date_high)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.frame_2)
        self.label_20 = QtWidgets.QLabel(search_panel)
        self.label_20.setObjectName("label_20")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.frame_20 = QtWidgets.QFrame(search_panel)
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_20)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.genres_text = QtWidgets.QLineEdit(self.frame_20)
        self.genres_text.setObjectName("genres_text")
        self.verticalLayout_12.addWidget(self.genres_text)
        self.genres_list = QtWidgets.QListWidget(self.frame_20)
        self.genres_list.setObjectName("genres_list")
        self.verticalLayout_12.addWidget(self.genres_list)
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.frame_20)
        self.label_21 = QtWidgets.QLabel(search_panel)
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.frame_21 = QtWidgets.QFrame(search_panel)
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_21)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.tags_text = QtWidgets.QLineEdit(self.frame_21)
        self.tags_text.setObjectName("tags_text")
        self.verticalLayout_13.addWidget(self.tags_text)
        self.tags_list = QtWidgets.QListWidget(self.frame_21)
        self.tags_list.setObjectName("tags_list")
        self.verticalLayout_13.addWidget(self.tags_list)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.frame_21)
        self.frame_3 = QtWidgets.QFrame(search_panel)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.submit_button = QtWidgets.QPushButton(self.frame_3)
        self.submit_button.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        self.submit_button.setFont(font)
        self.submit_button.setObjectName("submit_button")
        self.horizontalLayout_4.addWidget(self.submit_button)
        self.clear_button = QtWidgets.QPushButton(self.frame_3)
        self.clear_button.setMinimumSize(QtCore.QSize(0, 40))
        self.clear_button.setMaximumSize(QtCore.QSize(50, 16777215))
        self.clear_button.setObjectName("clear_button")
        self.horizontalLayout_4.addWidget(self.clear_button)
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.SpanningRole, self.frame_3)

        self.retranslateUi(search_panel)
        QtCore.QMetaObject.connectSlotsByName(search_panel)

    def retranslateUi(self, search_panel):
        _translate = QtCore.QCoreApplication.translate
        search_panel.setWindowTitle(_translate("search_panel", "Frame"))
        self.label_14.setText(_translate("search_panel", "Advanced Search"))
        self.filter_prev_button.setText(_translate("search_panel", "Prev"))
        self.filter_text.setText(_translate("search_panel", "AND (+, &)"))
        self.filter_next_button.setText(_translate("search_panel", "Next"))
        self.label_15.setText(_translate("search_panel", "Title"))
        self.label_16.setText(_translate("search_panel", "Artists"))
        self.label_17.setText(_translate("search_panel", "Series"))
        self.label_18.setText(_translate("search_panel", "Order"))
        self.order_number.setToolTip(_translate("search_panel", "0 will be treated as any order number"))
        self.label_19.setText(_translate("search_panel", "Rating"))
        self.rating_toggle.setText(_translate("search_panel", "include higher ratings?"))
        self.label.setText(_translate("search_panel", "Pages"))
        self.frame.setToolTip(_translate("search_panel", "0 pages will be treated as any page count"))
        self.label_3.setText(_translate("search_panel", "to"))
        self.label_2.setText(_translate("search_panel", "Date"))
        self.frame_2.setToolTip(_translate("search_panel", "9/14/1752 12:00 AM will be treated as any date"))
        self.label_4.setText(_translate("search_panel", "to"))
        self.label_20.setText(_translate("search_panel", "Genres"))
        self.label_21.setText(_translate("search_panel", "Tags"))
        self.submit_button.setText(_translate("search_panel", "Filter"))
        self.clear_button.setText(_translate("search_panel", "Clear"))
