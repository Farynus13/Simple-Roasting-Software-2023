from PySide6.QtWidgets import QLCDNumber
from PySide6.QtCore import QTime, QTimer, SIGNAL
class TemperatureLCD(QLCDNumber):
    def __init__(self,modbus,unit_id,parent = None):
        super(TemperatureLCD, self).__init__(parent)
        self.setSegmentStyle(QLCDNumber.Filled)

        self.modbus = modbus
        self.unit_id = unit_id
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'),self.showTemp)
        timer.start(100)
        self.showTemp()
        

    #reads temperature from slave with unit_id 1=bt_temp 2=et_temp
    def showTemp(self):
        temperature = self.modbus.read_temp(self.unit_id)
        self.display(temperature)