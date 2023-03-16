# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/metadata_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_metadata_panel(object):
    def setupUi(self, metadata_panel):
        metadata_panel.setObjectName("metadata_panel")
        metadata_panel.resize(1600, 900)
        self.verticalLayout = QtWidgets.QVBoxLayout(metadata_panel)
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtWidgets.QLabel(metadata_panel)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(24)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.frame = QtWidgets.QFrame(metadata_panel)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_11 = QtWidgets.QFrame(self.frame)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_10 = QtWidgets.QLabel(self.frame_11)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.frame_12 = QtWidgets.QFrame(self.frame_11)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.artists_text = QtWidgets.QLineEdit(self.frame_12)
        self.artists_text.setObjectName("artists_text")
        self.horizontalLayout_4.addWidget(self.artists_text)
        self.artists_submit = QtWidgets.QPushButton(self.frame_12)
        self.artists_submit.setObjectName("artists_submit")
        self.horizontalLayout_4.addWidget(self.artists_submit)
        self.verticalLayout_8.addWidget(self.frame_12)
        self.artists_list = QtWidgets.QListWidget(self.frame_11)
        self.artists_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.artists_list.setObjectName("artists_list")
        self.verticalLayout_8.addWidget(self.artists_list)
        self.horizontalLayout.addWidget(self.frame_11)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.frame_13 = QtWidgets.QFrame(self.frame)
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.frame_13)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_11.addWidget(self.label_11)
        self.frame_14 = QtWidgets.QFrame(self.frame_13)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_14)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.series_text = QtWidgets.QLineEdit(self.frame_14)
        self.series_text.setObjectName("series_text")
        self.horizontalLayout_5.addWidget(self.series_text)
        self.series_submit = QtWidgets.QPushButton(self.frame_14)
        self.series_submit.setObjectName("series_submit")
        self.horizontalLayout_5.addWidget(self.series_submit)
        self.verticalLayout_11.addWidget(self.frame_14)
        self.series_list = QtWidgets.QListWidget(self.frame_13)
        self.series_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.series_list.setObjectName("series_list")
        self.verticalLayout_11.addWidget(self.series_list)
        self.horizontalLayout.addWidget(self.frame_13)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.frame_15 = QtWidgets.QFrame(self.frame)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_12 = QtWidgets.QLabel(self.frame_15)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_10.addWidget(self.label_12)
        self.frame_16 = QtWidgets.QFrame(self.frame_15)
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.genres_text = QtWidgets.QLineEdit(self.frame_16)
        self.genres_text.setObjectName("genres_text")
        self.horizontalLayout_6.addWidget(self.genres_text)
        self.genres_submit = QtWidgets.QPushButton(self.frame_16)
        self.genres_submit.setObjectName("genres_submit")
        self.horizontalLayout_6.addWidget(self.genres_submit)
        self.verticalLayout_10.addWidget(self.frame_16)
        self.genres_list = QtWidgets.QListWidget(self.frame_15)
        self.genres_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.genres_list.setObjectName("genres_list")
        self.verticalLayout_10.addWidget(self.genres_list)
        self.horizontalLayout.addWidget(self.frame_15)
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.frame_17 = QtWidgets.QFrame(self.frame)
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_17)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_13 = QtWidgets.QLabel(self.frame_17)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_9.addWidget(self.label_13)
        self.frame_18 = QtWidgets.QFrame(self.frame_17)
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_18)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.tags_text = QtWidgets.QLineEdit(self.frame_18)
        self.tags_text.setObjectName("tags_text")
        self.horizontalLayout_7.addWidget(self.tags_text)
        self.tags_submit = QtWidgets.QPushButton(self.frame_18)
        self.tags_submit.setObjectName("tags_submit")
        self.horizontalLayout_7.addWidget(self.tags_submit)
        self.verticalLayout_9.addWidget(self.frame_18)
        self.tags_list = QtWidgets.QListWidget(self.frame_17)
        self.tags_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tags_list.setObjectName("tags_list")
        self.verticalLayout_9.addWidget(self.tags_list)
        self.horizontalLayout.addWidget(self.frame_17)
        self.line_4 = QtWidgets.QFrame(self.frame)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.traits_text = QtWidgets.QLineEdit(self.frame_3)
        self.traits_text.setObjectName("traits_text")
        self.horizontalLayout_2.addWidget(self.traits_text)
        self.traits_submit = QtWidgets.QPushButton(self.frame_3)
        self.traits_submit.setObjectName("traits_submit")
        self.horizontalLayout_2.addWidget(self.traits_submit)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.traits_list = QtWidgets.QListWidget(self.frame_2)
        self.traits_list.setObjectName("traits_list")
        self.verticalLayout_2.addWidget(self.traits_list)
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(metadata_panel)
        QtCore.QMetaObject.connectSlotsByName(metadata_panel)

    def retranslateUi(self, metadata_panel):
        _translate = QtCore.QCoreApplication.translate
        metadata_panel.setWindowTitle(_translate("metadata_panel", "Frame"))
        self.label_9.setText(_translate("metadata_panel", "Metadata"))
        self.label_10.setText(_translate("metadata_panel", "Artists"))
        self.artists_submit.setText(_translate("metadata_panel", "Create"))
        self.artists_list.setSortingEnabled(True)
        self.label_11.setText(_translate("metadata_panel", "Series"))
        self.series_submit.setText(_translate("metadata_panel", "Create"))
        self.series_list.setSortingEnabled(True)
        self.label_12.setText(_translate("metadata_panel", "Genres"))
        self.genres_submit.setText(_translate("metadata_panel", "Create"))
        self.genres_list.setSortingEnabled(True)
        self.label_13.setText(_translate("metadata_panel", "Tags"))
        self.tags_submit.setText(_translate("metadata_panel", "Create"))
        self.tags_list.setSortingEnabled(True)
        self.label.setText(_translate("metadata_panel", "Character Traits"))
        self.traits_submit.setText(_translate("metadata_panel", "Create"))
