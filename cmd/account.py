import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from database import sign_in_func, sign_up_func


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
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
            if sign_in_func(username, password) == []:
                self.label_2.setText(f'Неверный пароль или имя пользователя')
            else:
                print("Successfully logged in with username: ", username, "and password:", password)

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
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
                sign_up_func((username, password))
                print("Successfully created acc with username: ", username, "and password: ", password)
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.label_2.setText('Пароли не совпадают')

    def canselfunc(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DataBaseConnect(QDialog):
    def __init__(self):
        super(DataBaseConnect, self).__init__()
        loadUi("templates/databaseconnect.ui", self)
        self.connect.clicked.connect(self.connectfunc)
        self.tryconnect.clicked.connect(self.tryconnectfunc)
        self.localhost.clicked.connect(self.localhostfunc)

    def connectfunc(self):
        pass

    def tryconnectfunc(self):
        pass

    def localhostfunc(self):
        self.host.setText("localhost")
        self.port.setText("5432")
        self.username.setText("postgres")

    # app = QApplication(sys.argv)


# mainwindow = Login()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(mainwindow)
# widget.show()
# app.exec_()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(DataBaseConnect())
    widget.show()
    sys.exit(app.exec())
