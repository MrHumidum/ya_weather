from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStandardItemModel, QStandardItem
import io, os, sys, requests
from dotenv import load_dotenv
import psycopg2
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


# class Pogoda(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi('template.ui', self)
#         f = io.StringIO('template.ui')
#         self.pushButton.clicked.connect(self.run)
#         self.tableView.setModel(QStandardItemModel())
#         self.con = connect_to_database
#
#
#     def run(self):
#         info = (openweathermap(self.poisk.displayText()))
#         # self.history_city.append(self.poisk.text())
#         self.label.setText(f'{info}')

class Pogoda(QMainWindow):
    def __init__(self):
        super().__init()
        uic.loadUi('template.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.table_view = self.findChild(QTableView, 'tableView')  # Находит QTableView по имени

        # Создаем модель данных для QTableView
        self.model = QStandardItemModel(self)

    def run(self):
        city_name = self.poisk.displayText()
        weather_info = openweathermap(city_name)
        self.label.setText(f'Погода: {weather_info["Погода"]}, Температура: {weather_info["Температура"]}')
        insert_weather((city_name, weather_info["Температура"], weather_info["Погода"]))

        # Загрузите данные из базы данных
        data = get_weather()

        # Очистите модель данных
        self.model.clear()

        # Устанавливаем заголовки для столбцов
        self.model.setHorizontalHeaderLabels(["Город", "Температура", "Погода"])

        # Заполните модель данными из базы данных
        for row in data:
            items = [QStandardItem(str(item)) for item in row]
            self.model.appendRow(items)

        # Устанавливаем модель данных для QTableView
        self.table_view.setModel(self.model)


# a = {'icoid': data['weather'][0]['icon'],
#                 "City": city_name,
#                 "conditions": data['weather'][0]['description'],
#                 "temp": data['main']['temp']}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Pogoda()
    p.show()
    sys.exit(app.exec())
