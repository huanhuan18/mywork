from src.getColor import Ui_Form
# from PyQt5.Qt import *
from PyQt5.Qt import Qt, QColorDialog, QColor
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore
from pynput.mouse import Listener
import PyWinMouse as mouse
import qtawesome as qta

import sys, threading


class Mainpane(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)

        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("取色器")
        # 设置图标
        self.setWindowIcon(qta.icon('fa.eyedropper'))
        self.colorSelectPanel.setIcon(qta.icon('fa.contao', color="purple"))
        self.get_color_btn.setIcon(qta.icon('fa.paint-brush', color="red"))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.mouse = mouse.Mouse()
        # self.resize(600, 300)

    def keyPressEvent(self, event):
        """检测键盘Alt按键"""
        # print("按下：" + str(event.key()))
        if (event.key() == Qt.Key_Alt):
            # print('测试：Alt')
            x = self.mouse.get_mouse_pos()[0]
            y = self.mouse.get_mouse_pos()[1]
            self.getValue(x, y)

    def on_click(self, x, y, button, pressed):
        """监听鼠标点击"""
        # print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        self.getValue(x, y)
        if not pressed:
            # Stop listener
            return False

    def getValue(self, x, y):
        # 截取屏幕图片
        pixmap = QApplication.primaryScreen().grabWindow(0)
        # 获取鼠标点击地方的值
        image = pixmap.toImage()
        color = QColor(image.pixel(x, y))
        r, g, b = color.red(), color.green(), color.blue()
        strRGB = str(r) + ", " + str(g) + ", " + str(b)
        # print("strRGB", strRGB)
        hexs = list(map(lambda x: str(hex(x)).replace('0x', ''), [r, g, b]))
        strCSS = '#{:0>2s}{:0>2s}{:0>2s}'.format(*hexs)
        # print("strCSS", strCSS)
        self.rgbValue.setText(strRGB)
        self.cssValue.setText(strCSS)
        self.posValue.setText("x:{}  y:{}".format(x, y))
        self.colorShow.setStyleSheet("background-color: {};".format(strCSS))

    def openColorPanel(self):
        """获得调色盘的颜色值"""
        # 取消置顶
        self.setWindowFlags(QtCore.Qt.Widget)
        # 创建调色板
        c = QColorDialog.getColor()
        print(c.name())
        print(c.getRgb())
        self.cssValue.setText(c.name())
        self.rgbValue.setText(str(c.getRgb()[0])+", "+str(c.getRgb()[1])+", "+str(c.getRgb()[2]))
        self.posValue.setText("")
        self.colorShow.setStyleSheet("background-color: {};".format(c.name()))
        # 重新置顶
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()  # 不加这句窗口点完就会消失

    def changeMouseStyle(self):
        """改变鼠标样式并获取各项值"""
        # print("pass")
        self.setCursor(Qt.ClosedHandCursor)
        # x = QCursor.pos().x()
        # y = QCursor.pos().y()
        # xy = QCursor.pos()
        # print(x, y, xy)
        t = threading.Thread(target=self.listen)
        t.start()

    def listen(self):
        with Listener(on_click=self.on_click) as listener:
        # with Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            listener.join()

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    login_pane = Mainpane()
    login_pane.show()
    sys.exit(app.exec_())
