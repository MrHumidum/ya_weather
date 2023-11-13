from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView
from database import get_weather, insert_weather
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from database import sign_in_func, sign_up_func, openweathermap
import psycopg2
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.web_view = QWebEngineView()

        layout.addWidget(self.web_view)
        self.setCentralWidget(central_widget)

        # Load the local HTML file
        self.load_html_content()

    def load_html_content(self):
        self.web_view.setUrl(QUrl.fromLocalFile(
            "C:/Users/moydo/PycharmProjects/pythonProject/leaflet-openweathermap-master/example/index.html"))



class Pogoda(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/template.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.static)
        self.table_view = self.findChild(QTableView, 'tableView')

        self.model = QStandardItemModel(self)

    def static(self):
        global window1
        window1 = MyWindow()
        window1.show()

    def run(self):
        city_name = self.poisk.displayText()
        weather_info = openweathermap(city_name)
        if weather_info is None:
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


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        loadUi("templates/login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        if username == '' or password == '':
            self.label_2.setText('Заполните все поля')
        else:
            if not sign_in_func(username, password):
                self.label_2.setText(f'Неверный пароль или имя пользователя')
            else:
                print("Successfully logged in with username: ", username, "and password:", password)
                global p
                p = Pogoda()
                self.close()
                p.show()

    def gotocreate(self):
        global create
        create = CreateAcc()
        self.close()
        create.show()


class CreateAcc(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("templates/sign_up.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.canselbuttom.clicked.connect(self.canselfunc)

    def createaccfunction(self):
        username = self.username.text()
        password = self.password.text()
        confirmpass = self.confirmpass.text()
        if username == '' or password == '' or confirmpass == '':
            self.label_2.setText('Заполните все поля')
        elif len(password) < 8:
            self.label_2.setText('Пароль должен быть больше 8 символов')
        elif ' ' in password:
            self.label_2.setText('Пароль не должен содержать пробел')
        else:
            if self.password.text() == self.confirmpass.text():
                a = sign_up_func((username, password))
                if a == 'username':
                    self.label_2.setText('Имя пользователя занято')
                    return
                print("Successfully created acc with username: ", username, "and password: ", password)
                global login1
                login1 = Login()
                self.close()
                login1.show()
            else:
                self.label_2.setText('Пароли не совпадают')

    def canselfunc(self):
        global login1
        login1 = Login()
        self.close()
        login1.show()


class DataBaseConnect(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("templates/databaseconnect.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.hostt.clicked.connect(self.hostfunc)
        self.connect.clicked.connect(self.connectfunc)
        self.tryconnect.clicked.connect(self.tryconnectfunc)
        self.localhost.clicked.connect(self.localhostfunc)

        self.connect.setEnabled(False)

        self.host.textChanged.connect(self.check_input)
        self.username.textChanged.connect(self.check_input)
        self.password.textChanged.connect(self.check_input)
        self.databasename.textChanged.connect(self.check_input)
        self.port.textChanged.connect(self.check_input)

    def check_input(self):
        self.label_3.setText('Connect button is not available')
        self.connect.setEnabled(False)

    def connectfunc(self):
        dbtxt = open('txts/databasetxt.txt', 'w+')
        host1, user1, password1, port1 = self.host.text(), self.username.text(), self.password.text(), self.port.text()
        database1 = self.databasename.text()
        dbtxt.write(f'{host1}, {user1}, {password1}, {port1}, {database1}')
        dbtxt.close()
        global login
        login = Login()
        login.show()
        self.close()

    def tryconn(self):
        try:
            conn = psycopg2.connect(
                host=self.host.text(),
                user=self.username.text(),
                password=self.password.text(),
                database=self.databasename.text(),
                port=self.port.text()
            )
            conn.autocommit = True
            return conn
        except Exception as e:
            print('Error tryconn:', e)
            return None

    def tryconnectfunc(self):
        conn = self.tryconn()
        if conn:
            self.label_3.setText('Connect button is available')
            print(conn)
            self.connect.setEnabled(True)
            conn.close()
        else:
            self.label_3.setText('Connect button is not available')
            self.connect.setEnabled(False)

    def localhostfunc(self):
        self.host.setText("localhost")
        self.port.setText("5432")
        self.username.setText("postgres")

    def hostfunc(self):
        self.host.setText("0.tcp.eu.ngrok.io")
        self.port.setText("14870")
        self.username.setText("postgres")
        self.databasename.setText('weatherforecast')
        self.password.setText('1')
