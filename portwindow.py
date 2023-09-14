from PySide6.QtWidgets import QLabel, QVBoxLayout,QHBoxLayout, QWidget, QComboBox,QLineEdit, QPushButton,QGridLayout
from modbus import *
import serial.tools.list_ports

class PortWindow(QWidget):
    def __init__(self,modbus):
        super().__init__()
        self.setFixedSize(800,400)
        self.setWindowTitle("Port")

        self.modbus = modbus
        #modbus parameters 
        self.com_port_label = QLabel("Com Port : ")
        self.baud_rate_label = QLabel("Baud Rate : ")
        self.byte_size_label = QLabel("Byte Size : ")
        self.parity_label = QLabel("Parity : ")
        self.stop_bits_label = QLabel("Stop Bits : ")
        self.timeout_label = QLabel("Timeout(s) : ")

        self.com_port_combo_box = QComboBox(self)
        self.baud_rate_combo_box = QComboBox(self)
        self.byte_size_combo_box = QComboBox(self)
        self.parity_combo_box = QComboBox(self)
        self.stop_bits_combo_box = QComboBox(self)
        self.timeout_line_edit = QLineEdit(self)

        #getting list of parameters
        com_ports = [comport.device for comport in serial.tools.list_ports.comports()]
        for comm in  com_ports:
            self.com_port_combo_box.addItem(comm)
        for baud in BAUD_RATE_list :
            self.baud_rate_combo_box.addItem(str(baud))
        for byte_size in BYTE_SIZE_list :
            self.byte_size_combo_box.addItem(str(byte_size))
        for parity in PARITY_list :
            self.parity_combo_box.addItem(str(parity))
        for stop_bits in STOP_BITS_list : 
            self.stop_bits_combo_box.addItem(str(stop_bits))

        #setting default values to show
        try:
            self.com_port_combo_box.setCurrentIndex(com_ports.index(modbus.com_port))
        except ValueError:
            print("Com port not in list")
            self.com_port_combo_box.setCurrentIndex(0)

        self.baud_rate_combo_box.setCurrentIndex(BAUD_RATE_list.index(modbus.baud_rate))  
        self.byte_size_combo_box.setCurrentIndex(BYTE_SIZE_list.index(modbus.byte_size))
        self.parity_combo_box.setCurrentIndex(PARITY_list.index(modbus.parity))
        self.stop_bits_combo_box.setCurrentIndex(STOP_BITS_list.index(modbus.stop_bits))
        self.timeout_line_edit.setText(str(modbus.timeout))
        #slave parameters
        self.input1_label = QLabel("Input 1")
        self.input2_label = QLabel("Input 2")

        self.slave_label = QLabel("Slave : ")
        self.register_label = QLabel("Register : ")
        self.modbus_function_label = QLabel("Modbus Function : ")
        self.divider_label = QLabel("Divider : ")
        self.mode_label = QLabel("Mode : ")

        self.slave1_line_edit = QLineEdit(self)
        self.register1_line_edit = QLineEdit(self)
        self.modbus_function1_combo_box = QComboBox(self)
        self.divider1_combo_box = QComboBox(self)
        self.mode1_combo_box = QComboBox(self)

        self.slave2_line_edit = QLineEdit(self)
        self.register2_line_edit = QLineEdit(self)
        self.modbus_function2_combo_box = QComboBox(self)
        self.divider2_combo_box = QComboBox(self)
        self.mode2_combo_box = QComboBox(self)

        for mod_function in MODBUS_FUNCTION_list :
            self.modbus_function1_combo_box.addItem(str(mod_function))
            self.modbus_function2_combo_box.addItem(str(mod_function))
        for divider in DIVIDER_list :
            self.divider1_combo_box.addItem(str(divider))
            self.divider2_combo_box.addItem(str(divider))
        for mode in MODE_list :
            self.mode1_combo_box.addItem(mode)
            self.mode2_combo_box.addItem(mode)

        #setting values to show
        self.slave1_line_edit.setText(str(modbus.slave[0]))
        self.slave2_line_edit.setText(str(modbus.slave[1]))
        self.register1_line_edit.setText(str(modbus.register[0]))
        self.register2_line_edit.setText(str(modbus.register[1]))
        self.modbus_function1_combo_box.setCurrentIndex(MODBUS_FUNCTION_list.index(modbus.modbus_function[0]))
        self.modbus_function2_combo_box.setCurrentIndex(MODBUS_FUNCTION_list.index(modbus.modbus_function[1]))
        self.divider1_combo_box.setCurrentIndex(DIVIDER_list.index(modbus.divider[0]))
        self.divider2_combo_box.setCurrentIndex(DIVIDER_list.index(modbus.divider[1]))
        self.mode1_combo_box.setCurrentIndex(MODE_list.index(modbus.mode[0]))
        self.mode1_combo_box.setCurrentIndex(MODE_list.index(modbus.mode[1]))

        #setting values from modbus

        #buttons
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.ok_clicked)
        cancel_button = QPushButton("CANCEL")
        cancel_button.clicked.connect(self.cancel_clicked)

        #layout
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.com_port_label,0,0,1,1)
        self.grid_layout.addWidget(self.baud_rate_label,1,0,1,1)
        self.grid_layout.addWidget(self.byte_size_label,2,0,1,1)
        self.grid_layout.addWidget(self.parity_label,3,0,1,1)
        self.grid_layout.addWidget(self.stop_bits_label,4,0,1,1)
        self.grid_layout.addWidget(self.timeout_label,5,0,1,1)
        self.grid_layout.addWidget(self.com_port_combo_box,0,1,1,1)
        self.grid_layout.addWidget(self.baud_rate_combo_box,1,1,1,1)
        self.grid_layout.addWidget(self.byte_size_combo_box,2,1,1,1)
        self.grid_layout.addWidget(self.parity_combo_box,3,1,1,1)
        self.grid_layout.addWidget(self.stop_bits_combo_box,4,1,1,1)
        self.grid_layout.addWidget(self.timeout_line_edit,5,1,1,1)
        self.grid_layout.addWidget(self.input1_label,0,4,1,1)
        self.grid_layout.addWidget(self.slave_label,1,3,1,1)
        self.grid_layout.addWidget(self.register_label,2,3,1,1)
        self.grid_layout.addWidget(self.modbus_function_label,3,3,1,1)
        self.grid_layout.addWidget(self.divider_label,4,3,1,1)
        self.grid_layout.addWidget(self.mode_label,5,3,1,1)
        self.grid_layout.addWidget(self.slave1_line_edit,1,4,1,1)
        self.grid_layout.addWidget(self.register1_line_edit,2,4,1,1)
        self.grid_layout.addWidget(self.modbus_function1_combo_box,3,4,1,1)
        self.grid_layout.addWidget(self.divider1_combo_box,4,4,1,1)
        self.grid_layout.addWidget(self.mode1_combo_box,5,4,1,1)
        self.grid_layout.addWidget(self.input2_label,0,5,1,1)
        self.grid_layout.addWidget(self.slave2_line_edit,1,5,1,1)
        self.grid_layout.addWidget(self.register2_line_edit,2,5,1,1)
        self.grid_layout.addWidget(self.modbus_function2_combo_box,3,5,1,1)
        self.grid_layout.addWidget(self.divider2_combo_box,4,5,1,1)
        self.grid_layout.addWidget(self.mode2_combo_box,5,5,1,1)
        self.grid_layout.addWidget(ok_button,6,4,1,1)
        self.grid_layout.addWidget(cancel_button,6,5,1,1)
        self.setLayout(self.grid_layout)

    def ok_clicked(self):
        print("ok clicked")
        self.modbus.com_port = self.com_port_combo_box.currentText()
        self.modbus.baud_rate = int(self.baud_rate_combo_box.currentText())
        self.modbus.byte_size = int(self.byte_size_combo_box.currentText())
        self.modbus.parity = self.parity_combo_box.currentText()
        self.modbus.stop_bits = int(self.stop_bits_combo_box.currentText())
        self.modbus.timeout = float(self.timeout_line_edit.text())
        
        self.modbus.slave[0] = int(self.slave1_line_edit.text())
        self.modbus.slave[1] = int(self.slave2_line_edit.text())
        self.modbus.register[0] = int(self.register1_line_edit.text())
        self.modbus.register[1] = int(self.register2_line_edit.text())
        self.modbus.modbus_function[0] = int(self.modbus_function1_combo_box.currentText())
        self.modbus.modbus_function[1] = int(self.modbus_function2_combo_box.currentText())
        self.modbus.divider[0] = float(self.divider1_combo_box.currentText())
        self.modbus.divider[1] = float(self.divider2_combo_box.currentText())
        self.modbus.mode[0] = self.mode1_combo_box.currentText()
        self.modbus.mode[1] = self.mode2_combo_box.currentText()

        self.close()

    def cancel_clicked(self):
        print("cancel clicked")
        self.close()

