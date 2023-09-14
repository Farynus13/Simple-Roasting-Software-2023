from contextlib import nullcontext
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QSlider, QLabel, QLCDNumber
from PySide6.QtCore import *
from temperaturelcd import TemperatureLCD
from rorlcd import RorLCD
from timelcd import TimeLCD
from roastingplot import RoastPlot
from PySide6.QtGui import QFont, QColor
class CentralWidget(QWidget):
    def __init__(self,modbus):
        super().__init__()
        slider_value_font = QFont('Arial',18)
        #modbus
        self.modbus = modbus

        #air slider
        self.air_slider = QSlider(Qt.Vertical)
        self.air_slider.setMinimum(20)
        self.air_slider.setMaximum(50)
        self.air_slider.setValue(20)
        self.air_slider.valueChanged.connect(self.respond_to_air_slider)
        self.air_label = QLabel("AIR")
        self.air_value_label = QLabel("20")
        self.air_value_label.setFont(slider_value_font)
        self.air_slider.show()

        #drum slider
        self.drum_slider = QSlider(Qt.Vertical)
        self.drum_slider.setMinimum(20)
        self.drum_slider.setMaximum(50)
        self.drum_slider.setValue(20)
        self.drum_slider.valueChanged.connect(self.respond_to_drum_slider)
        self.drum_label = QLabel("DRUM")
        self.drum_value_label = QLabel("20")
        self.drum_value_label.setFont(slider_value_font)
        self.drum_slider.show()
        
        #burner slider
        self.burner_slider = QSlider(Qt.Vertical)
        self.burner_slider.setMinimum(0)
        self.burner_slider.setMaximum(100)
        self.burner_slider.setValue(0)
        self.burner_slider.valueChanged.connect(self.respond_to_burner_slider)
        self.burner_label = QLabel("BURNER")
        self.burner_value_label = QLabel("0")
        self.burner_value_label.setFont(slider_value_font)
        self.burner_slider.show()

        self.communication_status = QLabel("Communication status")
        self.connection_button = QPushButton("Start")
        self.connection_button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.connection_button.clicked.connect(self.set_modbus_connection)
        self.et_label = QLabel("ET")
        self.bt_label = QLabel("BT")
        self.et_ror_label = QLabel("ET ROR")
        self.bt_ror_label = QLabel("BT ROR")
        self.et_lcd = None
        self.bt_lcd = None
        self.et_ror_lcd = None
        self.bt_ror_lcd = None
        self.time_lcd = None
        #plotting temperatures
        self.roasting_plot = RoastPlot(self.bt_lcd,self.et_lcd,self.et_ror_lcd,self.bt_ror_lcd)
        self.plot = self.roasting_plot.plot
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.air_label,0,0,1,1)
        self.grid_layout.addWidget(self.air_value_label,1,0,1,1)
        self.grid_layout.addWidget(self.air_slider,2,0,6,1)
        self.grid_layout.addWidget(self.drum_label,8,0,1,1)
        self.grid_layout.addWidget(self.drum_value_label,9,0,1,1)
        self.grid_layout.addWidget(self.drum_slider,10,0,6,1)
        self.grid_layout.addWidget(self.burner_label,0,1,1,1)
        self.grid_layout.addWidget(self.burner_value_label,1,1,1,1)
        self.grid_layout.addWidget(self.burner_slider,2,1,14,1)
        self.grid_layout.addWidget(self.communication_status,0,3,1,15)
        self.grid_layout.addWidget(self.connection_button,0,23,2,2)
        self.grid_layout.addWidget(self.plot,1,2,16,21)

        self.setLayout(self.grid_layout)


    def respond_to_air_slider(self):
        self.air_value_label.setText(str(self.air_slider.value()))
        self.modbus.write_slave_register(5,8193,int(self.air_slider.value()))
    def respond_to_drum_slider(self):
        self.drum_value_label.setText(str(self.drum_slider.value()))
        self.modbus.write_slave_register(4,8193,int(self.drum_slider.value()))

    def respond_to_burner_slider(self):
        self.burner_value_label.setText(str(self.burner_slider.value()))

    def set_modbus_connection(self):
        if self.connection_button.text() == "Start" : 
            self.modbus_connect()
        elif self.connection_button.text() == "Stop" :
            self.connection_button.setText("Start")
            self.modbus_disconnect()
    def modbus_disconnect(self):
        print("disconnecting")
        self.roasting_plot.stop_plotting()
        self.time_lcd.stopTime()

    def modbus_connect(self):
        self.delete_old_widgets()
        self.modbus.connect_slaves()
        self.communication_status.setText("Successfully connected to modbus!")
        self.connection_button.setText("Stop")

        self.et_lcd = TemperatureLCD(self.modbus,2)
        self.bt_lcd = TemperatureLCD(self.modbus,1)
        self.et_ror_lcd = RorLCD(self.et_lcd,1)
        self.bt_ror_lcd = RorLCD(self.bt_lcd,2)
        self.time_lcd = TimeLCD()

        self.grid_layout.addWidget(self.time_lcd,2,23,2,2)
        self.grid_layout.addWidget(self.et_label,4,23,1,2)
        self.grid_layout.addWidget(self.bt_label,7,23,1,2)
        self.grid_layout.addWidget(self.et_ror_label,10,23,1,2)
        self.grid_layout.addWidget(self.bt_ror_label,13,23,1,2)
        self.grid_layout.addWidget(self.bt_ror_lcd,14,23,2,2)
        self.grid_layout.addWidget(self.et_ror_lcd,11,23,2,2)
        self.grid_layout.addWidget(self.bt_lcd,8,23,2,2)
        self.grid_layout.addWidget(self.et_lcd,5,23,2,2)

        self.roasting_plot.bt_lcd = self.bt_lcd
        self.roasting_plot.et_lcd = self.et_lcd
        self.roasting_plot.bt_ror_lcd = self.bt_ror_lcd
        self.roasting_plot.et_ror_lcd = self.et_ror_lcd

        self.roasting_plot.start_plotting()
        self.time_lcd.startTime()

    def delete_old_widgets(self) :
        if self.et_lcd != None :
            self.et_lcd.deleteLater()
        if self.bt_lcd != None :
            self.bt_lcd.deleteLater()
        if self.et_ror_lcd != None :
            self.et_ror_lcd.deleteLater()
        if self.bt_ror_lcd != None :
            self.bt_ror_lcd.deleteLater()
        if self.time_lcd != None :
            self.time_lcd.deleteLater()