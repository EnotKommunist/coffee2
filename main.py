import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection = sqlite3.connect("coffe.db")
        query = "SELECT * FROM coffee"
        res = self.connection.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.pushButton.clicked.connect(self.save_results)
        self.pushButton_2.clicked.connect(self.add_in_tabel)

    def add_in_tabel(self):
        query = f"INSERT INTO table_name ('id', 'sort_name', 'roasting', 'ground/in grains', 'taste description', 'coast', 'packing volume') VALUES ({self.lineEdit_1.text()}, {self.lineEdit_2.text()}, {self.lineEdit_3.text()}, {self.lineEdit_5.text()}, {self.lineEdit_4.text()}, {self.lineEdit_7.text()}, {self.lineEdit_6.text()})"
        res = self.connection.cursor().execute(query).fetchall()

    def save_results(self):
        pass

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())