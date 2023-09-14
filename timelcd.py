from PySide6.QtWidgets import QLCDNumber
from PySide6.QtCore import QTime, QTimer, SIGNAL
class TimeLCD(QLCDNumber):
    def __init__(self,parent = None):
        super(TimeLCD, self).__init__(parent)
        self.setSegmentStyle(QLCDNumber.Filled)
        self.time_counter = 0

    def showTime(self):
        text = ""
        self.time_counter+=1
        s = self.time_counter%60
        m = int(self.time_counter/60)
        text += str(m) + ":" + str(s)
        self.display(text)

    def startTime(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.showTime)
        self.timer.start()

    def stopTime(self):
        self.timer.stop()
        self.time_counter = 0


