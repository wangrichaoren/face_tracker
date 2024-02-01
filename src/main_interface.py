# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import time
from PyQt5.QtGui import QColor, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSettings, Qt, QDateTime
from qfluentwidgets import setFont, MessageBox, FluentIcon, PlainTextEdit
import cv2
import numpy as np
from view.ui_main import Ui_Main
from src.servo_manager import ServoManager, ServoEnum
from src.camera_manager import CameraManager
from src.trancking_plot1 import trancking_plot1
from src.trancking_plot2 import trancking_plot2

"""
    主程序界面
"""


class MainInterface(Ui_Main, QWidget):
    stop_debug_servo = pyqtSignal()
    stop_debug_camera = pyqtSignal()
    sys_running_sign = pyqtSignal(bool)
    log_sign = pyqtSignal(int, str, name="log_sign")  # 日志信号 0-正常 1-异常 2-错误
    face_tracking_sign = pyqtSignal(list)
    clear_view_sign = pyqtSignal()

    def __init__(self, face_detector, camera_manager, servo_manager, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.isRunning = False
        self.isTracking = False

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
        self.log_te = PlainTextEdit(self)
        self.log_te.setReadOnly(True)
        self.log_te.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.log_te.setFocusPolicy(Qt.NoFocus)
        self.HeaderCardWidget.viewLayout.setContentsMargins(5, 5, 5, 5)
        self.HeaderCardWidget.viewLayout.addWidget(self.log_te)

        self.tra1RadioButton.setEnabled(False)
        self.tra2RadioButton.setEnabled(False)

        # 连接槽函数
        self.connectSignSlots()

    def connectSignSlots(self):
        self.sysButton.clicked.connect(self.sysBtnClickedSlot)
        self.log_sign.connect(self.logSlot, Qt.QueuedConnection)
        self.face_tracking_sign.connect(self.faceTracking, Qt.DirectConnection)

        self.clear_view_sign.connect(self.clearViewSlot, Qt.DirectConnection)

    def clearViewSlot(self):
        self.frameview.setPixmap(
            QPixmap("resource/image/trans.png").scaled(self.frameview.size(), aspectRatioMode=True))

    def trackingFunc_1(self, info):
        x, y, w, h = info
        center_x = int(w / 2)
        center_y = int(h / 2)
        dif_x = x - center_x
        dif_y = y - center_y
        """
        * 当dif_x>0时，代表底部舵机该往右转;
        * 当dif_x<0时，代表底部舵机该往左转;
        * 当dif_y>0时，代表上部舵机该往下转;
        * 当dif_y<0时，代表上部舵机该往上转.
        """

        """
        策略一: 根据dif的大小，限定step
        1280/10=128
        720/10=72
        """
        # todo 可以根据人脸大小的策略....  切割画面 分更多段搞
        x_thread = 40
        y_thread = x_thread
        # nums = [1, 8, 12]
        nums = [2, 10, 20]

        if abs(dif_x) < x_thread:
            x_step = 0
        elif x_thread <= abs(dif_x) <= w / 2 * 1 / 3:
            x_step = nums[0]
        elif w / 2 * 1 / 3 < abs(dif_x) <= w / 2 * 2 / 3:
            x_step = nums[1]
        else:
            x_step = nums[2]

        if abs(dif_y) < y_thread:
            y_step = 0
        elif abs(dif_y) <= h / 2 * 1 / 3:
            # y_step = 1
            y_step = int(nums[0] * 0.5625)
        elif h / 2 * 1 / 3 < abs(dif_y) <= h / 2 * 2 / 3:
            y_step = int(nums[1] * 0.5625)
        else:
            y_step = int(nums[2] * 0.5625)

        if dif_x > 0 and dif_y > 0:
            # 底部舵机右转(+)&上部舵机下转(+)
            # print("底部舵机右转(+)&上部舵机下转(+)")
            self.servo_manager.moveA(x_step, y_step)
        elif dif_x < 0 and dif_y > 0:
            # 底部舵机左转(-)&上部舵机下转(+)
            # print("底部舵机左转(-)&上部舵机下转(+)")
            self.servo_manager.moveA(-x_step, y_step)
        elif dif_x > 0 and dif_y < 0:
            # 底部舵机右转(+)&上部舵机上转(-)
            # print("底部舵机右转(+)&上部舵机上转(-)")
            self.servo_manager.moveA(x_step, -y_step)
        elif dif_x < 0 and dif_y < 0:
            # 底部舵机左转(-)&上部舵机上转(-)
            # print("底部舵机左转(-)&上部舵机上转(-)")
            self.servo_manager.moveA(-x_step, -y_step)

    def trackingFunc_2(self, info):
        pass

    def faceTracking(self, info):
        assert isinstance(self.servo_manager, ServoManager)
        if not self.isRunning:
            return
        if self.tra1RadioButton.isChecked():
            trancking_plot1(info, self.servo_manager)
        else:
            trancking_plot2(info, self.servo_manager)

    def logSlot(self, idx, msg):
        cur_time = QDateTime.currentDateTime().toString("yyyy-MM-dd-hh:mm:ss")  # 获取当前时间
        if idx == 0:
            display_msg = """
                            <html>
                            <body>
                            <p><strong>{}: {}</strong></p>
                            </body>
                            </html>
                            """.format(cur_time, msg)
        elif idx == 1:
            display_msg = """
                         <html>
                         <body>
                         <p><strong><span style="color:orange;">{}: [警告] {}</span></strong></p>
                         </body>
                         </html>
                         """.format(cur_time, msg)
        else:
            display_msg = """
                         <html>
                         <body>
                         <p><strong><span style="color:red;">{}: [异常] {}</span></strong></p>
                         </body>
                         </html>
                         """.format(cur_time, msg)
        self.log_te.appendHtml(display_msg)

    def sysBtnClickedSlot(self):
        assert isinstance(self.servo_manager, ServoManager)
        assert isinstance(self.camera_manager, CameraManager)
        if self.isRunning:
            self.log_sign.emit(0, "点击关闭系统按钮.")
            self.isRunning = False
            self.servo_manager.disconnectSerial()
            self.camera_manager.disconnect()
            self.sys_running_sign.emit(False)
            self.camera_manager.update_frame_sign.disconnect()
            self.clear_view_sign.emit()
            self.tra1RadioButton.setEnabled(False)
            self.tra2RadioButton.setEnabled(False)
            self.log_sign.emit(0, "系统已关闭.")
            self.sysButton.setText("一键启动系统")
        else:
            self.log_sign.emit(0, "点击一键启动系统按钮.")
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
            self.isRunning = True
            self.servo_manager.connectSerial(self.settings.value("ServoIdx"))
            self.log_sign.emit(0, "舵机连接成功.")
            self.camera_manager.connect(int(self.settings.value("CamIdx")))
            self.camera_manager.update_frame_sign.connect(self.updateFrameSlot, Qt.DirectConnection)
            self.tra1RadioButton.setEnabled(True)
            self.tra2RadioButton.setEnabled(True)
            self.log_sign.emit(0, "相机连接成功.")
            self.sysButton.setText("暂停系统")

    def updateFrameSlot(self, frame):
        _frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        # 推理
        res, keyp, _frame = self.face_detector.inference(_frame)
        h = _frame.shape[0]
        w = _frame.shape[1]
        cv2.line(_frame, (0, int(h / 2)), (w, int(h / 2)), (255, 0, 0), 1)
        cv2.line(_frame, (int(w / 2), 0), (int(w / 2), h), (0, 0, 255), 1)

        # 将关键点发出去
        if keyp:
            self.face_tracking_sign.emit([*keyp, _frame.shape[1], _frame.shape[0]])

        _image = QImage(_frame[:], _frame.shape[1], _frame.shape[0], _frame.shape[1] * 3,
                        QImage.Format_RGB888)
        _out = QPixmap(_image)
        # 调整图片尺寸以适应label大小，并更新label上的图片显示
        self.frameview.setPixmap(_out.scaled(self.frameview.size(), aspectRatioMode=True))

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 100))
        shadowEffect.setBlurRadius(30)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)
