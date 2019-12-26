import queue
import sys
import threading
import json
import datetime
from requests.exceptions import ConnectionError
import css

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from weather_response import weather_response


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.city_desc_label = QLabel()
        self.time_label = QLabel()
        self.temp_label = QLabel()
        self.loading_gif_movie = QMovie("icons/loading.gif")

        self.input_textbox = MainWindow.InputTextBox("", self, self)
        self.error_label = QLabel()

        self.coord_label = QLabel()
        self.weather_icon_label = QLabel()
        self.wind_label = QLabel()

        self.request_queue = queue.Queue()
        self.forecast_thread = threading.Thread(target=self.forecast,
                                                args=(self.request_queue,))
        self.response = None

        self.init_window()

    def init_window(self):
        self.setWindowIcon(QIcon("icons/forecaster_logo.png"))
        self.setWindowTitle("Forecaster")
        self.setFixedSize(600, 350)
        self.setStyleSheet("QMainWindow {background-image: url('icons/forecaster-first_view.jpg'); "
                           "background-position: center;}")

        self.create_layout()
        self.forecast_thread.start()
        self.show()

    def create_layout(self):
        grid_layout = QGridLayout()

        grid_layout.addWidget(self.top_row(), 0, 0, Qt.AlignCenter)
        grid_layout.addWidget(self.mid_row(), 1, 0)
        grid_layout.addWidget(self.bot_row(), 2, 0)

        group_box = QGroupBox("What is the weather like in...?")
        group_box.setLayout(grid_layout)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(group_box)

        central_widget = QWidget()
        central_widget.setLayout(vbox_layout)

        self.setCentralWidget(central_widget)

    def top_row(self):
        vbox_layout = QVBoxLayout()

        self.city_desc_label.setFixedSize(150, 50)
        self.city_desc_label.setStyleSheet(css.common_label_large_text)
        self.city_desc_label.setAlignment(Qt.AlignCenter)
        vbox_layout.addWidget(self.city_desc_label)
        vbox_layout.setAlignment(self.city_desc_label, Qt.AlignCenter)

        self.time_label.setAlignment(Qt.AlignCenter)
        vbox_layout.addWidget(self.time_label)
        vbox_layout.setAlignment(self.time_label, Qt.AlignCenter)

        self.temp_label.setFixedSize(30, 30)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.loading_gif_movie.setScaledSize(self.temp_label.size())
        self.loading_gif_movie.start()
        vbox_layout.addWidget(self.temp_label)
        vbox_layout.setAlignment(self.temp_label, Qt.AlignCenter)

        top_row_widget = QWidget()
        top_row_widget.setLayout(vbox_layout)

        return top_row_widget

    def mid_row(self):
        grid_layout = QGridLayout()

        self.error_label.setStyleSheet("color: red")
        grid_layout.addWidget(self.error_label, 0, 0)

        self.input_textbox.setText("Look for a location")
        self.input_textbox.setToolTip("City name/ID, Zip code or coordinates")
        self.input_textbox.setStyleSheet("background-color: rgba(255, 255, 255, 150);"
                                         "border: 0px;")
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.darkGray)
        self.input_textbox.setPalette(palette)
        self.input_textbox.returnPressed.connect(self.request_weather)
        self.input_textbox.setMinimumHeight(30)
        grid_layout.addWidget(self.input_textbox, 1, 0)

        forecast_button = QPushButton(QIcon("icons/search.png"), "", self)
        forecast_button.setToolTip("Get forecast")
        forecast_button.setMinimumHeight(30)
        forecast_button.clicked.connect(self.request_weather)
        grid_layout.addWidget(forecast_button, 1, 1)

        mid_row_widget = QWidget()
        mid_row_widget.setLayout(grid_layout)

        return mid_row_widget

    def bot_row(self):
        hbox_layout = QHBoxLayout()

        self.coord_label.setStyleSheet(css.common_label_small_text)
        self.coord_label.setAlignment(Qt.AlignCenter)
        self.coord_label.setFixedSize(130, 80)
        hbox_layout.addWidget(self.coord_label)

        self.weather_icon_label.setStyleSheet(css.common_label_small_text)
        self.weather_icon_label.setAlignment(Qt.AlignCenter)
        self.weather_icon_label.setFixedSize(130, 80)
        hbox_layout.addWidget(self.weather_icon_label)

        self.wind_label.setStyleSheet(css.common_label_small_text)
        self.wind_label.setAlignment(Qt.AlignCenter)
        self.wind_label.setFixedSize(130, 80)
        self.wind_label.setStyleSheet(self.wind_label.styleSheet() +
                                      "background-image: url('icons/forecaster_logo.jpg'); "
                                      "background-position: center;")
        hbox_layout.addWidget(self.wind_label)

        bot_row_widget = QWidget()
        bot_row_widget.setLayout(hbox_layout)

        return bot_row_widget

    def request_weather(self):
        self.error_label.clear()
        self.temp_label.setMovie(self.loading_gif_movie)

        self.request_queue.put(self.input_textbox.text())

    def forecast(self, request_queue):
        while True:
            try:
                response = None
                try:
                    response = json.loads(weather_response(request_queue.get()))
                except TypeError:
                    pass
                self.refresh(response)
            except ConnectionError as exc:
                self.error_label.setText("No connection to the internet. Please check your connection")
                print(exc)

    def refresh(self, response):
        if response is not None:
            internal_code = str(response["cod"])
            if internal_code[0] == "3":
                self.error_label.setText("There seems to be a problem...")
            elif internal_code == "404":
                self.error_label.setText("The location could not be found. Please try a different one.")
            elif internal_code[0] == "4":
                self.error_label.setText("Failed to connect to service.")
            elif internal_code[0] == "5":
                self.error_label.setText("The weather service seems to be unavailable. Please try again later.")
            else:
                self.load_ui(response)
                self.response = response
        else:
            if self.response is not None:
                self.load_ui(self.response)

    def load_ui(self, response):

        if "name" in response and response["name"] != "":
            city_desc = response["name"] + ", " + response["sys"]["country"]
        else:
            city_desc = "somewhere out " + "\n" + \
                        "there..."
        self.city_desc_label.setText(city_desc)

        curr_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=response["timezone"])
        self.time_label.setText(curr_time.ctime())
        self.temp_label.setText(str(int(response["main"]["temp"])) + u"\u2103")

        self.coord_label.setText("Lon: " + str(response["coord"]["lon"]) + "\n" +
                                 "Lat: " + str(response["coord"]["lat"]))
        self.weather_icon_label.setPixmap(QPixmap("icons/weather/" + response["weather"][0]["icon"] + "@2x.png"))
        self.wind_label.setText(str(response["wind"]["speed"]) + " Beaufort")

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
