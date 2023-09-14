import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QMainWindow, QApplication,QVBoxLayout, QWidget
from PySide6.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.tight_layout()
        super(MplCanvas, self).__init__(fig)


class RoastPlot(QWidget):

    def __init__(self,bt_lcd,et_lcd,et_ror_lcd,bt_ror_lcd):
        super(RoastPlot, self).__init__()

        self.bt_lcd = bt_lcd
        self.et_lcd = et_lcd
        self.et_ror_lcd = et_ror_lcd
        self.bt_ror_lcd = bt_ror_lcd

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.xdata = []
        self.bt_y = []
        self.et_y = []
        self.et_ror_y = []
        self.bt_ror_y = []
        
        self.counter = 0
        self.canvas.draw()

        toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        self.plot = QWidget()
        self.plot.setLayout(layout)



    def update_plot(self):
        # Drop off the first y element, append a new one.
        bt = self.bt_lcd.value()
        et = self.et_lcd.value()
        bt_ror = self.bt_ror_lcd.value()
        et_ror = self.et_ror_lcd.value()

        self.bt_y.append(float(bt))
        self.et_y.append(float(et))
        self.et_ror_y.append(float(et_ror))
        self.bt_ror_y.append(float(bt_ror))

        self.xdata.append(self.counter/200)
        self.counter+=1
        
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.bt_y, self.xdata,self.et_y,self.xdata,self.bt_ror_y,self.xdata,self.et_ror_y)
        self.canvas.axes.set_xlim([0,15])
        self.canvas.axes.set_ylim([0,220])

        # Trigger the canvas to update and redraw.
        self.canvas.draw()

     # Setup a timer to trigger the redraw by calling update_plot.
    def start_plotting(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
    def stop_plotting(self):
        self.timer.stop()
        self.xdata = []
        self.bt_y = []
        self.et_y = []
        self.bt_ror_y = []
        self.et_ror_y = []
        self.counter = 0
