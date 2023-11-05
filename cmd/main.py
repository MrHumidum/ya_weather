from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
import io, os, sys, requests
from dotenv import load_dotenv
import psycopg2

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
        uic.loadUi('template.ui', self)
        f = io.StringIO('template.ui')
        self.pushButton.clicked.connect(self.run)

    def run(self):
        info = (openweathermap(self.poisk.displayText()))
        # self.history_city.append(self.poisk.text())
        self.label.setText(f'{info}')


# a = {'icoid': data['weather'][0]['icon'],
#                 "City": city_name,
#                 "conditions": data['weather'][0]['description'],
#                 "temp": data['main']['temp']}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Pogoda()
    p.show()
    sys.exit(app.exec())
