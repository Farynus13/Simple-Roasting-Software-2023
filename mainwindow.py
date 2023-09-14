from PySide6.QtWidgets import QMainWindow,QStatusBar, QGridLayout,QVBoxLayout,QHBoxLayout, QSlider, QLabel, QWidget
from PySide6.QtGui import QAction,QScreen
from PySide6.QtCore import *
from portwindow import PortWindow
from eventwindow import EventWindow
from centralwidget import CentralWidget
from modbus import Modbus

class MainWindow(QMainWindow):
    def __init__(self,app,modbus,width,height):
        super().__init__()
        self.app = app # declare an app member
        self.setWindowTitle("Floppster - Roasting Dumminess")
        self.setGeometry(0,0,width,height)

        self.modbus = modbus

        #actions
        port_action = QAction("Port",self)
        port_action.setStatusTip("Opens Port Configuration Window")
        port_action.triggered.connect(self.open_port_window)
       
        event_action = QAction("Event",self)
        event_action.setStatusTip("Opens Event Configuration Window")
        event_action.triggered.connect(self.open_event_window)

        #Menu bar
        menu_bar = self.menuBar()

        #file menu
        file_menu = menu_bar.addMenu("File")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        
        #edit menu
        edit_menu = menu_bar.addMenu("Edit")

        #config menu
        config_menu = menu_bar.addMenu("Config")

        self.port_window = None
        config_menu.addAction(port_action)
        self.event_window = None
        config_menu.addAction(event_action)

        #status bar
        self.setStatusBar(QStatusBar(self))

        #main panel layout
        central_widget = CentralWidget(self.modbus)
        self.setCentralWidget(central_widget)
        self.show()
    
        
        
    def open_port_window(self, checked):
        if self.port_window is None:
            self.port_window = PortWindow(self.modbus)
            self.port_window.show()
        else:
            self.port_window.close()  # Close window.
            self.port_window = None  # Discard reference.

    def open_event_window(self, checked):
        if self.event_window is None:
            self.event_window = EventWindow()
            self.event_window.show()
        else:
            self.event_window.close()  # Close window.
            self.event_window = None  # Discard reference.
            
    def quit_app(self):
        self.app.quit()