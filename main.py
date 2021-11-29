import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection = sqlite3.connect("coffe.db")
        cur = self.connection.cursor()
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
        self.pushButton_2.clicked.connect(self.add_in_tabel)
        self.tableWidget.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row, column):
        item_change = self.tableWidget.currentItem().text()
        rows = list(set(map(lambda x: x.row(), self.tableWidget.selectedItems())))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(self, '', f"Действительно заменить элементы с id {', '.join(ids)}",
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.connection.cursor()
            for i in ids:
                data = cur.execute(f"SELECT * FROM coffee WHERE id = {i}").fetchone()
                new_data = list(data)
                new_data[column] = item_change
                new_data = tuple(new_data)
                cur.execute(f"DELETE FROM coffee WHERE id = {i}")
                cur.execute("INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)", new_data)
            self.connection.commit()

    def add_in_tabel(self):
        cursor = self.connection.cursor()
        id = self.lineEdit.text()
        sort_name = self.lineEdit_2.text()
        roasting = self.lineEdit_3.text()
        ground_grains = self.lineEdit_5.text()
        taste_description = self.lineEdit_4.text()
        coast = self.lineEdit_7.text()
        packing_volume = self.lineEdit_6.text()
        cursor.execute(f"""INSERT INTO coffee VALUES ({int(id)}, '{sort_name}', '{roasting}', '{ground_grains}', '{taste_description}', '{coast}', '{packing_volume}')""")
        self.connection.commit()


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())