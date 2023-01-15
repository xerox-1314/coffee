import concurrent.futures
import sys
import sqlite3 as sq
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QWidget

connect = sq.connect('coffee_db.db')
cursor = connect.cursor()

def get_coffee():
    result = cursor.execute('SELECT sort, number_roast, type, taste, price, package FROM coffee').fetchall()
    return result

def update(column, value, id):
    cursor.execute(f"""UPDATE coffee 
    SET {column} = '{value}'
    WHERE ID = '{id}'""")
    connect.commit()

def add(sort, number_roast, type, taste, price, package):
    cursor.execute(f"""INSERT INTO coffee (sort, number_roast, type, taste, price, package) VALUES ('{sort}', '{number_roast}', '{type}', '{taste}', '{price}', '{package}')""")
    connect.commit()


class CoffeeView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Coffee Display')
        self.change_dict = ['Сорт', 'Степень обжарки', 'Молотый/В зернах', 'Описание вкуса', 'Цена', 'Объем упаковки']
        self.edit_but.clicked.connect(self.edit)
        self.add_but.clicked.connect(self.add)
        self.reset_but.clicked.connect(self.reset)
        self.view_table()

    def view_table(self):
        info = get_coffee()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(self.change_dict)
        for i, row in enumerate(info):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def edit(self):
        self.ec = EditCoffee()
        self.ec.show()

    def add(self):
        self.ac = AddCoffee()
        self.ac.show()

    def reset(self):
        self.view_table()


class EditCoffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('EditCoffeeForm.ui', self)
        self.setWindowTitle('Coffee Edit')
        self.change_dict = ['Сорт', 'Степень обжарки', 'Молотый/В зернах', 'Описание вкуса', 'Цена', 'Объем упаковки']
        self.columns_list = ['sort', 'number_roast', 'type', 'taste', 'price', 'package']
        self.ok_but.clicked.connect(self.ok)
        self.cancel_but.clicked.connect(self.cancel)
        self.view_table()

    def view_table(self):
        info = get_coffee()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(self.change_dict)
        for i, row in enumerate(info):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def ok(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    value = item.text()
                    column = self.columns_list[j]
                    update(column, value, i + 1)

    def cancel(self):
        self.close()


class AddCoffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addCoffeeForm.ui', self)
        self.setWindowTitle('Coffee Add')
        self.type.addItems(['Молотый', 'В зернах'])
        self.ok_but.clicked.connect(self.ok)
        self.cancel_but.clicked.connect(self.cancel)

    def ok(self):
        if self.sort.text() == '' or self.number_roast.text() == '' or self.type.currentText() == '' or self.taste.text() == '' or self.price.text() == '' or self.package_2.text() == '':
            self.error_message.setText('Заполните все поля')
        else:
            add(self.sort.text(), self.number_roast.text(), self.type.currentText(), self.taste.text(), self.price.text(), self.package_2.text())
            self.close()

    def cancel(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeView()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
