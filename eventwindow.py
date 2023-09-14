from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

class EventWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Event Window")
        layout.addWidget(self.label)
        self.setLayout(layout)