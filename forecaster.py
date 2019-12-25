import queue
import sys
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from weather_response import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.input_textbox = MainWindow.InputTextBox("", self, self)
        self.error_label = QLabel()
        self.request_queue = queue.Queue()
        self.request_thread = threading.Thread(target=self.forecast,
                                               args=(self.request_queue,))

        self.init_window()

    def init_window(self):
        self.setWindowIcon(QIcon("icons/forecaster_logo.png"))
        self.setWindowTitle("Forecaster")
        self.setFixedSize(600, 350)
        self.setStyleSheet("QMainWindow {background-image: url('icons/forecaster-first_view.jpg'); "
                           "background-position: center;}")

        self.create_layout()
        self.request_thread.start()
        self.show()

    def create_layout(self):
        grid_layout = QGridLayout()
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(3, 1)

        self.error_label.setStyleSheet("color: red")
        grid_layout.addWidget(self.error_label, 1, 0)

        self.input_textbox.setText("Look for a location")
        self.input_textbox.setToolTip("City name/ID, Zip code or coordinates")
        self.input_textbox.setStyleSheet("background-color: rgba(255, 255, 255, 150);"
                                         "border: 0px;")
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.darkGray)
        self.input_textbox.setPalette(palette)
        self.input_textbox.returnPressed.connect(self.request_weather)
        self.input_textbox.setMinimumHeight(30)
        grid_layout.addWidget(self.input_textbox, 2, 0)

        forecast_button = QPushButton(QIcon("icons/search.png"), "", self)
        forecast_button.setToolTip("Get forecast")
        forecast_button.setMinimumHeight(30)
        forecast_button.clicked.connect(self.request_weather)
        grid_layout.addWidget(forecast_button, 2, 1)

        group_box = QGroupBox("What is your desired forecast?")
        group_box.setLayout(grid_layout)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(group_box)

        central_widget = QWidget()
        central_widget.setLayout(vbox_layout)

        self.setCentralWidget(central_widget)

    def request_weather(self):
        self.error_label.setText("")
        self.request_queue.put(self.input_textbox.text())

    def forecast(self, queue):
        while True:
            try:
                response = return_current_weather_data_by_city_name(queue.get())
                print(response)
            except:
                self.error_label.setText("No connection to internet. Please check your connection")

    class InputTextBox(QLineEdit):

        def __init__(self, contents, parent, outer_instance):
            super().__init__(contents, parent)
            self.outer_instance = outer_instance

        def focusInEvent(self, event):
            palette = QPalette()
            palette.setColor(QPalette.Text, Qt.black)
            self.setPalette(palette)
            self.clear()
            super().focusInEvent(event)

        def focusOutEvent(self, event):
            palette = QPalette()
            palette.setColor(QPalette.Text, Qt.darkGray)
            self.setPalette(palette)
            self.setText("Look for a location")
            super().focusOutEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())
