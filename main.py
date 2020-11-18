import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Coffee")
        self.con = sqlite3.connect("coffee.sqlite")
        self.update_result()
        self.pushButton.clicked.connect(self.change)
        self.dialog = MyWidget2()
        self.dialog.pushButton.clicked.connect(self.update_result)
        self.dialog.pushButton_2.clicked.connect(self.update_result)

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Name", "Roasting", "Ground", "Taste", "Price", "Size"])
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def change(self):
        self.dialog.show()
        self.update_result()


class MyWidget2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("CoffeeEdit")
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.add_results)
        self.modified = []
        self.titles = None
        self.begin()

    def begin(self):
        self.id = []
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Name", "Roasting", "Ground", "Taste", "Price", "Size"])
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                if j == 0:
                    self.id.append(str(val))
        self.modified = []

    def update_result(self):
        if self.modified:
            cur = self.con.cursor()
            for i in self.modified:
                que = "UPDATE coffee SET\n"
                first = True
                for key in i.keys():
                    if not first:
                        que += ','
                    que += "{}='{}'\n".format(key, i.get(key))
                    first = False
                que += '\n where id == ' + i['ID']
                cur.execute(que)
                self.con.commit()
            self.modified.clear()
            self.begin()

    def item_changed(self, item):
        self.modified.append({})
        self.modified[-1][self.titles[item.column()]] = item.text()
        self.modified[-1]['ID'] = self.tableWidget.item(item.row(), 0).text()

    def add_results(self):
        self.statusBar.clearMessage()
        try:
            float(self.lineEdit_6.text())
            float(self.lineEdit_7.text())
            int(self.lineEdit.text())
        except ValueError:
            self.statusBar.showMessage("Некорректные данные")
        if (self.lineEdit_4.text() != "0") and (self.lineEdit_4.text() != "1") or (self.lineEdit.text() in self.id):
            self.statusBar.showMessage("Некорректные данные")
        else:
            s1 = self.lineEdit.text()
            s2 = self.lineEdit_2.text()
            s3 = self.lineEdit_3.text()
            s4 = self.lineEdit_4.text()
            s5 = self.lineEdit_5.text()
            s6 = self.lineEdit_6.text()
            s7 = self.lineEdit_7.text()
            cur = self.con.cursor()
            que = f"INSERT INTO coffee(Id, Name, Roasting, Ground, Taste, Price, Size)" \
                  f" VALUES({s1},'{s2}','{s3}',{s4},'{s5}',{s6},{s7})"
            cur.execute(que)
            self.con.commit()
        self.begin()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
