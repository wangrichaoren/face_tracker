# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal, QSettings, Qt
from qfluentwidgets import setFont, MessageBox, FluentIcon
import cv2
from view.ui_camera import Ui_Camera
from src.camera_manager import CameraManager
from src.face_detect_interface import FaceDetector

"""
    调试相机界面
"""


class CameraInterface(Ui_Camera, QWidget):
    update_frame_info_sign = pyqtSignal(int, int)

    def __init__(self, face_detector, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.face_detector = face_detector
        self._isCamOpen = False
        self._isDetOpen = False

        self._camera_manager = None

        self._settings = QSettings("config/setting.ini", QSettings.IniFormat)

        # 设置一下控件的文字大小
        setFont(self.camButton, 17)
        setFont(self.detButton, 17)
        setFont(self.nameLabel, 13)
        setFont(self.devLabel, 13)
        setFont(self.whBodyLabel, 13)
        setFont(self.posLabel, 13)

        self.refButton.setIcon(FluentIcon.SYNC)

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

        # 给个默认的相机
        self.chooseBox.addItem("相机 {}".format(self._settings.value("CamIdx")))

        # 设置控件阴影
        self.setShadowEffect(self.videoCardWidget)
        self.setShadowEffect(self.setCardWidget)
        self.setShadowEffect(self.infoCardWidget)

        self.detButton.setEnabled(False)

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
        self.settingButton.clicked.connect(self.settingCamIdxSlot)
        self.camButton.clicked.connect(self.openCamSlot)
        self.detButton.clicked.connect(self.detSlot)
        self.refButton.clicked.connect(self.refCamDrivers)

        self.update_frame_info_sign.connect(self.updateFrameInfoSlot)

    def refCamDrivers(self):
        """
        刷新相机设备数量
        :return:
        """
        self.chooseBox.clear()
        for i in self.getAllCameraDrives():
            self.chooseBox.addItem("相机 {}".format(i))

    def updateFrameInfoSlot(self, w, h):
        self.whLineEdit.setText("{}x{}".format(w, h))

    def openCamSlot(self):
        if not self._isCamOpen:
            if self._camera_manager is not None:
                return
            self._camera_manager = CameraManager()
            ret, msg = self._camera_manager.connect(int(self.chooseBox.currentText().split(" ")[1]))
            if not ret:
                w = MessageBox(
                    '相机启动失败',
                    '失败原因: {}.'.format(msg),
                    self
                )
                w.yesButton.setText('确定')
                w.cancelButton.setText('返回')
                w.exec()
                self._camera_manager = None
                return
            self._camera_manager.update_frame_sign.connect(self.updateFrame, Qt.DirectConnection)
            self.detButton.setEnabled(True)
            self.chooseBox.setEnabled(False)
            self.refButton.setEnabled(False)
            self.nameLineEdit.setText(self.chooseBox.currentText())
            self.devLineEdit.setText("cpu")
            self.update_frame_info_sign.emit(*self._camera_manager.getFrameWH())
            self.camButton.setText("关闭相机")
        else:
            if self._camera_manager is not None:
                self._camera_manager.disconnect()
                self._camera_manager.deleteLater()
                self._camera_manager = None
                self.detButton.setEnabled(False)
                self.chooseBox.setEnabled(True)
                self.refButton.setEnabled(True)
                self.nameLineEdit.setText("")
                self.whLineEdit.setText("")
                self.devLineEdit.setText("")
                self.posLineEdit.setText("")
                self.detButton.setText("开启视觉检测")
                self._isDetOpen = False
                self.camView.setPixmap(QPixmap())
            self.camButton.setText("开启相机")
        self._isCamOpen = not self._isCamOpen

    def updateFrame(self, frame):
        _frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        if self._isDetOpen:
            assert isinstance(self.face_detector, FaceDetector)
            res, _frame = self.face_detector.inference(_frame)
        _image = QImage(_frame[:], _frame.shape[1], _frame.shape[0], _frame.shape[1] * 3,
                        QImage.Format_RGB888)
        _out = QPixmap(_image)
        if self._isCamOpen:
            self.camView.setPixmap(_out)  # 设置图片显示
        else:
            self.camView.setPixmap(QPixmap())

    def detSlot(self):
        if not self._isDetOpen:
            self.detButton.setText("关闭视觉检测")
        else:
            self.detButton.setText("开启视觉检测")
        self._isDetOpen = not self._isDetOpen

    def settingCamIdxSlot(self):
        self._settings.setValue("CamIdx", self.chooseBox.currentText().split(" ")[1])

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 100))
        shadowEffect.setBlurRadius(30)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)
