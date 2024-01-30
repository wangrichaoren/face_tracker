# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_camera.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Camera(object):
    def setupUi(self, Camera):
        Camera.setObjectName("Camera")
        Camera.resize(552, 340)
        self.gridLayout = QtWidgets.QGridLayout(Camera)
        self.gridLayout.setObjectName("gridLayout")
        self.videoCardWidget = CardWidget(Camera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoCardWidget.sizePolicy().hasHeightForWidth())
        self.videoCardWidget.setSizePolicy(sizePolicy)
        self.videoCardWidget.setObjectName("videoCardWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.videoCardWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.camView = ImageLabel(self.videoCardWidget)
        self.camView.setObjectName("camView")
        self.gridLayout_3.addWidget(self.camView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.videoCardWidget, 0, 0, 1, 1)
        self.setCardWidget = CardWidget(Camera)
        self.setCardWidget.setObjectName("setCardWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.setCardWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.helpPlainTextEdit = PlainTextEdit(self.setCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.helpPlainTextEdit.setSizePolicy(sizePolicy)
        self.helpPlainTextEdit.setReadOnly(True)
        self.helpPlainTextEdit.setObjectName("helpPlainTextEdit")
        self.gridLayout_2.addWidget(self.helpPlainTextEdit, 0, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.chooseBox = ComboBox(self.setCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chooseBox.sizePolicy().hasHeightForWidth())
        self.chooseBox.setSizePolicy(sizePolicy)
        self.chooseBox.setMinimumSize(QtCore.QSize(0, 0))
        self.chooseBox.setObjectName("chooseBox")
        self.verticalLayout.addWidget(self.chooseBox)
        self.camButton = PushButton(self.setCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camButton.sizePolicy().hasHeightForWidth())
        self.camButton.setSizePolicy(sizePolicy)
        self.camButton.setMinimumSize(QtCore.QSize(0, 0))
        self.camButton.setObjectName("camButton")
        self.verticalLayout.addWidget(self.camButton)
        self.detButton = PushButton(self.setCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detButton.sizePolicy().hasHeightForWidth())
        self.detButton.setSizePolicy(sizePolicy)
        self.detButton.setMinimumSize(QtCore.QSize(0, 0))
        self.detButton.setObjectName("detButton")
        self.verticalLayout.addWidget(self.detButton)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.infoCardWidget = CardWidget(self.setCardWidget)
        self.infoCardWidget.setObjectName("infoCardWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.infoCardWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.posLabel = BodyLabel(self.infoCardWidget)
        self.posLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.posLabel.setObjectName("posLabel")
        self.gridLayout_4.addWidget(self.posLabel, 3, 0, 1, 1)
        self.fpsLabel = BodyLabel(self.infoCardWidget)
        self.fpsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fpsLabel.setObjectName("fpsLabel")
        self.gridLayout_4.addWidget(self.fpsLabel, 1, 0, 1, 1)
        self.whBodyLabel = BodyLabel(self.infoCardWidget)
        self.whBodyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.whBodyLabel.setObjectName("whBodyLabel")
        self.gridLayout_4.addWidget(self.whBodyLabel, 2, 0, 1, 1)
        self.nameLabel = BodyLabel(self.infoCardWidget)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout_4.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.nameLineEdit = LineEdit(self.infoCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLineEdit.sizePolicy().hasHeightForWidth())
        self.nameLineEdit.setSizePolicy(sizePolicy)
        self.nameLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLineEdit.setReadOnly(True)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout_4.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.fpsLineEdit = LineEdit(self.infoCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fpsLineEdit.sizePolicy().hasHeightForWidth())
        self.fpsLineEdit.setSizePolicy(sizePolicy)
        self.fpsLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.fpsLineEdit.setReadOnly(True)
        self.fpsLineEdit.setObjectName("fpsLineEdit")
        self.gridLayout_4.addWidget(self.fpsLineEdit, 1, 1, 1, 1)
        self.whLineEdit = LineEdit(self.infoCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.whLineEdit.sizePolicy().hasHeightForWidth())
        self.whLineEdit.setSizePolicy(sizePolicy)
        self.whLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.whLineEdit.setReadOnly(True)
        self.whLineEdit.setObjectName("whLineEdit")
        self.gridLayout_4.addWidget(self.whLineEdit, 2, 1, 1, 1)
        self.posLineEdit = LineEdit(self.infoCardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.posLineEdit.sizePolicy().hasHeightForWidth())
        self.posLineEdit.setSizePolicy(sizePolicy)
        self.posLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.posLineEdit.setReadOnly(True)
        self.posLineEdit.setObjectName("posLineEdit")
        self.gridLayout_4.addWidget(self.posLineEdit, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.infoCardWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.setCardWidget, 1, 0, 1, 1)

        self.retranslateUi(Camera)
        QtCore.QMetaObject.connectSlotsByName(Camera)

    def retranslateUi(self, Camera):
        _translate = QtCore.QCoreApplication.translate
        Camera.setWindowTitle(_translate("Camera", "Camera"))
        self.camButton.setText(_translate("Camera", "开启相机"))
        self.detButton.setText(_translate("Camera", "开启视觉检测"))
        self.posLabel.setText(_translate("Camera", "人脸位置"))
        self.fpsLabel.setText(_translate("Camera", "FPS"))
        self.whBodyLabel.setText(_translate("Camera", "图像宽高"))
        self.nameLabel.setText(_translate("Camera", "设备名"))
from qfluentwidgets import BodyLabel, CardWidget, ComboBox, ImageLabel, LineEdit, PlainTextEdit, PushButton
