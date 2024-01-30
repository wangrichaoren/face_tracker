# -*- coding:utf-8 -*-
import sys
from PyQt5.QtCore import Qt, QUrl, QSettings, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, isDarkTheme,
                            NavigationPushButton, NavigationWidget, SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from view.servo_interface import ServoInterface
from view.camera_interface import CameraInterface


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        # 加载配置文件
        self.settings = QSettings("config/setting.ini", QSettings.IniFormat)

        # 添加子界面
        self.mainInterface = Widget("主程序", self)
        self.cameraInterface = CameraInterface(self)
        self.servoInterface = ServoInterface(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.mainInterface, FIF.HOME, '主程序')
        self.addSubInterface(self.cameraInterface, FIF.ALBUM, '调试图像')
        self.addSubInterface(self.servoInterface, FIF.ROBOT, '调试舵机')

        self.navigationInterface.addItem(
            routeKey='avatar',
            icon='resource/image/avatar.png',
            text='Cola',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.addItem(
            routeKey='themeInterface',
            icon=FIF.BRIGHTNESS,
            text='明亮模式',
            position=NavigationItemPosition.BOTTOM,
            onClick=self.changeTheme,
            selectable=False,
        )

        self.navigationInterface.setCurrentItem(self.mainInterface.objectName())

    def changeTheme(self):
        if isDarkTheme():
            setTheme(Theme.LIGHT)
            m_text = "明亮模式"
            m_icon = FIF.BRIGHTNESS
            self.settings.setValue("ThemeMode", 0)
        else:
            setTheme(Theme.DARK)
            m_text = "夜间模式"
            m_icon = FIF.CONSTRACT
            self.settings.setValue("ThemeMode", 1)
        theme_it = self.navigationInterface.items["themeInterface"]
        if isinstance(theme_it, NavigationPushButton):
            theme_it._text = m_text
            theme_it._icon = m_icon

    def initWindow(self):
        # 缩放界面，设置界面图标和标题，移动到屏幕中间
        self.resize(1000, 800)
        self.setWindowIcon(QIcon('resource/image/logo.png'))
        self.setWindowTitle('Face Tracker')
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()

        if self.settings.value("ThemeMode") == "0":
            setTheme(Theme.LIGHT)
            m_text = "明亮模式"
            m_icon = FIF.BRIGHTNESS
        else:
            setTheme(Theme.DARK)
            m_text = "夜间模式"
            m_icon = FIF.CONSTRACT
        theme_it = self.navigationInterface.items["themeInterface"]
        if isinstance(theme_it, NavigationPushButton):
            theme_it._text = m_text
            theme_it._icon = m_icon
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        w = MessageBox(
            '项目介绍🍜',
            '该项目全称为基于视觉的人脸追踪云台,涵盖软件/硬件/算法等三大部分,可实现实时的人脸追踪效果,可应用于迎宾/安防/导购登诸多与人交互的应用场景🍤.\n如果觉得该项目做的还行,请点个赞呗🌼~',
            self
        )
        w.yesButton.setText(' 👍 * 10086')
        w.cancelButton.setText(' 👎 * 99999')
        w.exec()


if __name__ == '__main__':
    # 设置高分屏 高dpi
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
