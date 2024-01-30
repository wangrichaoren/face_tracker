# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from qfluentwidgets import FluentIcon, PushButton, PlainTextEdit, LineEdit, ComboBox, BodyLabel, setFont
import cv2

from view.ui_camera import Ui_Camera


class CameraInterface(Ui_Camera, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 设置一下控件的文字大小
        setFont(self.chooseBox, 16)
        setFont(self.camButton, 16)
        setFont(self.detButton, 16)
        setFont(self.nameLabel, 13)
        setFont(self.fpsLabel, 13)
        setFont(self.whBodyLabel, 13)
        setFont(self.posLabel, 13)

        # 设置帮助信息
        help_text = """
                <html>
                    <body>
                        <p><strong><font size="5">使用说明: \n</font></strong></p>
                        <p>● 请先选择目标相机,在执行开启相机; \n</p>
                        <p>● 如若选择的相机不对,请关闭相机后再重新选择并打开进行查看; \n</p>
                        <p>● 确定好选择的相机后,请点击设置相机号,以便云台追踪的相机号使用; \n</p>
                        <p>● 点击开启视觉检测,将会输出检测结果数据及检测图像. \n</p>
                    </body>
                </html>
                """
        self.helpPlainTextEdit.document().setHtml(help_text)

        # 扫描当前设备下的所有可用相机
        for i in self.getAllCameraDrives():
            self.chooseBox.addItem("相机 {}".format(i))

        # 设置控件阴影
        self.setShadowEffect(self.videoCardWidget)
        self.setShadowEffect(self.setCardWidget)
        self.setShadowEffect(self.infoCardWidget)

        # 连接槽函数
        self.connectSignSlots()

    def getAllCameraDrives(self):
        """
        扫描当前设备下的所有可用相机
        :return:
        """
        camera_devices = []
        for i in range(10):  # 假设最多检测10个设备
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_devices.append(i)
                cap.release()
        return camera_devices

    def connectSignSlots(self):
        pass

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 100))
        shadowEffect.setBlurRadius(30)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)
