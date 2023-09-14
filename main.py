from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow
import sys
from modbus import Modbus
from PySide6.QtGui import QGuiApplication

app = QApplication(sys.argv)
width,height = app.primaryScreen().size().toTuple()

modbus = Modbus()
window = MainWindow(app,modbus,width,height)

window.show()

app.exec()