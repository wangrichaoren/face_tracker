# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal, QSettings
from qfluentwidgets import setFont, MessageBox, FluentIcon
import cv2

from view.ui_main import Ui_Main

"""
    主程序界面
"""


class MainInterface(Ui_Main, QWidget):
    def __init__(self, face_detector, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        setFont(self.startButton, 20)
        setFont(self.stopButton, 20)

        # 设置控件阴影
        self.setShadowEffect(self.frameview)
        self.setShadowEffect(self.CardWidget)
        self.setShadowEffect(self.CardWidget_2)

        # 连接槽函数
        self.connectSignSlots()

    def connectSignSlots(self):
        # self.settingButton.clicked.connect(self.settingCamIdxSlot)
        # self.camButton.clicked.connect(self.openCamSlot)
        # self.detButton.clicked.connect(self.detSlot)
        # self.refButton.clicked.connect(self.refCamDrivers)
        #
        # self.update_frame_info_sign.connect(self.updateFrameInfoSlot)
        pass

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 100))
        shadowEffect.setBlurRadius(30)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)
