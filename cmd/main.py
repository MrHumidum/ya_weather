from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
import os, sys, requests
from dotenv import load_dotenv
from database import get_weather, insert_weather

load_dotenv()

MY_TOKEN = os.getenv("MY_TOKEN")


def openweathermap(city_name):
    appid = MY_TOKEN
    try:
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={appid}&lang=ru&units=metric")
        data = res.json()
        return {'icoid': data['weather'][0]['icon'],
                "Погода": data['weather'][0]['description'],
                "Температура": int(data['main']['temp'])}
    except Exception as e:
        print("Error openweathermap:", e)
        pass


class Pogoda(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/template.ui ', self)
        self.pushButton.clicked.connect(self.run)
        self.table_view = self.findChild(QTableView, 'tableView')

        self.model = QStandardItemModel(self)

    def run(self):
        city_name = self.poisk.displayText()
        weather_info = openweathermap(city_name)
        if weather_info == None:
            print('[ERROR] Некорректное название города')
            self.label.setText(f'[ERROR] Некорректное название города')
            self.label_2.setText(f'[ERROR] Некорректное название города')
        else:
            self.label.setText(f'Погода: {weather_info["Погода"]}')
            self.label_2.setText(f'Температура: {weather_info["Температура"]}°C')

            pixmap = QPixmap(f"ico/{weather_info['icoid']}@2x.png")
            self.label_picture.setPixmap(pixmap)
            self.label_picture.setScaledContents(True)
            insert_weather((city_name, weather_info["Температура"], weather_info["Погода"]))

            data = get_weather()

            self.model.clear()

            self.model.setHorizontalHeaderLabels(["Дата и время", "Город", "Температура", "Погода"])

            for row in data:
                items = [QStandardItem(str(item)) for item in row]
                self.model.appendRow(items)

            self.table_view.setModel(self.model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Pogoda()
    p.show()
    sys.exit(app.exec())
