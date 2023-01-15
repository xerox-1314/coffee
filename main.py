import sys
import sqlite3 as sq
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class CoffeeView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Coffee Display')
        self.change_dict = ['ID', 'Сорт', 'Степень обжарки', 'Молотый/В зернах', 'Описание вкуса', 'Цена', 'Объем упаковки']
        self.connect = sq.connect('coffee_db.db')
        self.cursor = self.connect.cursor()
        self.view_table()

    def get_coffee(self):
        result = self.cursor.execute('SELECT * FROM coffee').fetchall()
        print(result)
        return result

    def view_table(self):
        info = self.get_coffee()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(self.change_dict)
        for i, row in enumerate(info):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeView()
    ex.show()
    sys.exit(app.exec())
