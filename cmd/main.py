from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
from pyqtclasses import DataBaseConnect

app = QApplication(sys.argv)
Dialog = QtWidgets.QDialog()

db_connect = DataBaseConnect()
db_connect.show()

# Запускаем цикл приложения
sys.exit(app.exec_())


