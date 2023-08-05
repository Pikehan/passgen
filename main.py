from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
import sys

import MainWindow
import passgen
import options

class MainWidget(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.copy_button.setEnabled(False)
        self.generate_button.clicked.connect(self.generate_onclick)
        self.copy_button.clicked.connect(self.copy_onclick)
        self.add_to_list_button.clicked.connect(self.add_to_list)
        self.remove_from_list_button.clicked.connect(self.remove_from_list)

        self.pwd_list = []

        self.load_password()

    def load_password(self):
        try:
            with open("./passwords", mode="r") as F:
                lines = F.readlines()
            list_of_pwd = lines[0].split("|")
            self.pwd_list = list_of_pwd

            self.tableWidget.setRowCount(len(list_of_pwd))
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setColumnWidth(2, 300)

            for pwd_count in range(len(list_of_pwd)):
                self.tableWidget.setItem(pwd_count, 2, QTableWidgetItem(list_of_pwd[pwd_count]))

            self.remove_from_list_button.setEnabled(True)

        except:
            self.tableWidget.setRowCount(0)
            self.remove_from_list_button.setEnabled(False)

    def generate_onclick(self):
        self.set_password()

    def copy_onclick(self):
        QtGui.QGuiApplication.clipboard().setText(self.pwd_out.text())

    def add_to_list(self):
        self.pwd_list.append(self.pwd_out.text())

        with open("./passwords", mode="w+") as F:
            F.write("|".join(self.pwd_list))

        self.load_password()

    def remove_from_list(self):
        current_row = self.tableWidget.currentRow()

        try:
            self.pwd_list.remove(self.tableWidget.item(current_row, 2).text())
            with open("./passwords", mode="w+") as F:
                F.write("|".join(self.pwd_list))

            self.load_password()

        except Exception as e:
            print(e)

    def save_changes(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            projectName = self.tableWidget.item(currentQTableWidgetItem.row(), 0).text()

    def get_character(self):
        chars = ''

        for checkbox_ in options.Characters:
            if getattr(self, f"{checkbox_.name}Check").isChecked():
                chars += checkbox_.value

        return chars

    def set_password(self):
        if self.length_box.value() <= 3:
            self.pwd_out.setText("Length must be greater than 3")
            self.copy_button.setEnabled(False)
            self.add_to_list_button.setEnabled(False)
            return

        if not self.get_character():
            self.pwd_out.setText("Choose at least one option")
            self.copy_button.setEnabled(False)
            self.add_to_list_button.setEnabled(False)
            return

        try:
            generated_pwd = passgen.generate_password(
                pwd_length=self.length_box.value(),
                character=self.get_character())
            self.pwd_out.setText(generated_pwd)

            self.copy_button.setEnabled(True)
            self.add_to_list_button.setEnabled(True)

        except IndexError:
            self.pwd_out.clear()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        QApplication.clipboard().clear()


if __name__ == "__main__":
    app = QApplication([])

    main_widget = MainWidget()

    main_widget.show()

    sys.exit(app.exec())
