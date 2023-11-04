import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import io
import sys


def openweathermap(city_name):
    appid = "1cb355434ede36bb01e202c3bda0aa4a"
    try:
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={appid}&lang=ru&units=metric")
        data = res.json()
        print("City:", city_name)
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
        return data['weather'][0]['icon']
    except Exception as e:
        print("Exception (weather):", e)
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

    def initUI(self):
        self.label_picture = QLabel(self)
        pixmap = QPixmap(f"ico/01d@2x.png")
        self.label_picture.setPixmap(pixmap)
        self.pushButton.
        self.label_picture.setScaledContents(True)  # Растягиваем изображение, чтобы оно вписалось в QLabel


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Pogoda()
    p.show()
    sys.exit(app.exec())
