import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import io, os, sys
from dotenv import load_dotenv

load_dotenv()

MY_TOKEN = os.getenv("MY_TOKEN")


def openweathermap(city_name):
    appid = MY_TOKEN
    try:
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={appid}&lang=ru&units=metric")
        data = res.json()
        return {"Погода": data['weather'][0]['description'],
                "Температура": data['main']['temp']}
    except Exception as e:
        print(e)
        pass



template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>639</width>
    <height>456</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>639</width>
    <height>456</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>639</width>
    <height>456</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Погода</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLineEdit" name="poisk">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>290</y>
      <width>201</width>
      <height>21</height>
     </rect>
    </property>
   </widget>
   <widget class="QTextEdit" name="history_city">
    <property name="geometry">
     <rect>
      <x>320</x>
      <y>270</y>
      <width>301</width>
      <height>121</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_picture">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>20</y>
      <width>561</width>
      <height>171</height>
     </rect>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>215</y>
      <width>581</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>TextLabel</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>330</y>
      <width>71</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <family>Arial</family>
      <pointsize>13</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Вывод</string>
    </property>
    <property name="autoDefault">
     <bool>false</bool>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>639</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Pogoda(QMainWindow):
    def __init__(self):
        super().__init__()

        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        info = (openweathermap(self.poisk.displayText()))
        self.history_city.append(self.poisk.text())
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
