# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSettings, Qt
from qfluentwidgets import setFont, MessageBox, FluentIcon, PlainTextEdit
import cv2

from view.ui_main import Ui_Main
from src.face_detect_interface import FaceDetector
from src.servo_manager import ServoManager, ServoEnum
from src.camera_manager import CameraManager

"""
    主程序界面
"""


class MainInterface(Ui_Main, QWidget):
    stop_debug_servo = pyqtSignal()
    stop_debug_camera = pyqtSignal()
    sys_running_sign = pyqtSignal(bool)

    def __init__(self, face_detector, camera_manager, servo_manager, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.isRunning = False

        self.settings = QSettings("config/setting.ini", QSettings.IniFormat)

        self.face_detector = face_detector
        self.camera_manager = camera_manager
        self.servo_manager = servo_manager

        setFont(self.sysButton, 17)

        # 设置控件阴影
        self.setShadowEffect(self.frameview)
        self.setShadowEffect(self.CardWidget)
        self.setShadowEffect(self.CardWidget_2)
        self.setShadowEffect(self.HeaderCardWidget)

        self.helpPlainTextEdit.setFocusPolicy(Qt.NoFocus)

        self.sysButton.setShortcut("space")

        # 设置帮助信息
        help_text = """
                        <html>
                            <body>
                                <p><strong><font size="5">使用说明: \n</font></strong></p>
                                <p>● 点击一键启动系统按钮,即可一键启动人脸识别及云台追踪功能; \n</p>
                                <p>● 系统启动中,会自动检测硬件设备是否已连接上,请根据提示进行断连或继续操作; \n</p>
                                <p>● 系统启动后,其他子界面将会暂停使用,控件将回归到初始状态; \n</p>
                                <p>● 点击关闭系统按钮,子界面将恢复可操作状态,系统暂停. \n</p>
                            </body>
                        </html>
                        """
        self.helpPlainTextEdit.document().setHtml(help_text)
        self.HeaderCardWidget.setTitle("输出信息")
        self.HeaderCardWidget.headerView.setFixedHeight(40)
        log_te = PlainTextEdit(self)
        log_te.setReadOnly(True)
        log_te.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        log_te.setFocusPolicy(Qt.NoFocus)
        self.HeaderCardWidget.viewLayout.setContentsMargins(5, 5, 5, 5)
        self.HeaderCardWidget.viewLayout.addWidget(log_te)

        # 连接槽函数
        self.connectSignSlots()

    def connectSignSlots(self):
        self.sysButton.clicked.connect(self.sysBtnClickedSlot)

    def sysBtnClickedSlot(self):
        if self.isRunning:
            # todo 关闭逻辑
            self.sys_running_sign.emit(False)
            self.sysButton.setText("一键启动系统")

        else:
            assert isinstance(self.servo_manager, ServoManager)
            assert isinstance(self.camera_manager, CameraManager)
            if self.servo_manager.isAlive() + self.camera_manager.isAlive() > 0:
                w = MessageBox(
                    '注意✋',
                    '检测到【舵机】或【相机】设备仍处于连接状态,设备再连接状态下无法一键启动系统.\n是否一键断开所有连接并启动系统?',
                    self
                )
                w.yesButton.setText('断开并启动')
                w.cancelButton.setText('返回')
                if w.exec() == 1:
                    self.stop_debug_servo.emit()
                    self.stop_debug_camera.emit()
                else:
                    return
            self.sys_running_sign.emit(True)
            # todo 开启逻辑


            self.sysButton.setText("暂停系统")
        self.isRunning = not self.isRunning

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 100))
        shadowEffect.setBlurRadius(30)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)
