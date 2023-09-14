from PySide6.QtWidgets import QLCDNumber
from PySide6.QtCore import QTime, QTimer, SIGNAL
class RorLCD(QLCDNumber):
    def __init__(self,temp_lcd,unit_id,parent = None):
        super(RorLCD, self).__init__(parent)
        self.setSegmentStyle(QLCDNumber.Filled)
        
        self.temp_lcd = temp_lcd
        self.lastTemps = []
        for i in range(10) :
            self.lastTemps.append(0.0)

        self.unit_id = unit_id
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'),self.showRor)
        timer.start(100)
        self.showRor()
        

    #reads temperature from slave with unit_id 1=bt_temp 2=et_temp
    def showRor(self):
        new_temp = self.temp_lcd.value()
        self.lastTemps.pop(0)
        self.lastTemps.append(new_temp)
        ror = (self.lastTemps[9]-self.lastTemps[0])*10
        self.display(ror)