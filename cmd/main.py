from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
import io, os, sys, requests
from dotenv import load_dotenv
from database import connect_to_database, get_weather, insert_weather

load_dotenv()

MY_TOKEN = os.getenv("MY_TOKEN")
db_config = {'host': os.getenv("host"),
             'port': os.getenv("port"),
             'user': os.getenv("user"),
             'dbname': os.getenv("dbname"),
             'password': os.getenv("password")
             }


def openweathermap(city_name):
    appid = MY_TOKEN
    try:
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={appid}&lang=ru&units=metric")
        data = res.json()
        return {"Погода": data['weather'][0]['description'],
                "Температура": int(data['main']['temp'])}
    except Exception as e:
        print(e)
        pass


class Pogoda(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cmd/templates/template.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.table_view = self.findChild(QTableView, 'tableView')

        self.model = QStandardItemModel(self)

    def run(self):
        city_name = self.poisk.displayText()
        weather_info = openweathermap(city_name)
        self.label.setText(f'Погода: {weather_info["Погода"]}, Температура: {weather_info["Температура"]}')
        insert_weather((city_name, weather_info["Температура"], weather_info["Погода"]))

        data = get_weather()

        self.model.clear()

        self.model.setHorizontalHeaderLabels(["Город", "Температура", "Погода"])

        for row in data:
            items = [QStandardItem(str(item)) for item in row]
            self.model.appendRow(items)

        self.table_view.setModel(self.model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Pogoda()
    p.show()
    sys.exit(app.exec())
