from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
import sys
import json

import MainWindow
import passgen
import options
import crypt


class MainWidget(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tableWidget.setColumnWidth(2, 190)
        self.tableWidget.setColumnCount(3)
        self.copy_button.setEnabled(False)
        self.add_to_list_button.setEnabled(False)
        self.remove_from_list_button.setEnabled(False)

        self.copy_button.clicked.connect(self.copy_on_click)
        self.generate_button.clicked.connect(self.set_password)
        self.add_to_list_button.clicked.connect(self.pwd_dict)
        self.remove_from_list_button.clicked.connect(self.remove_from_dict)
        self.tableWidget.cellChanged.connect(self.add_to_dict)
        self.tableWidget.cellClicked.connect(self.pwd_show)

        self.tableData = []

        self.load_data()

    def copy_on_click(self):
        QtGui.QGuiApplication.clipboard().setText(self.pwd_out.text())

    def load_data(self):
        try:
            data = crypt.decrypt_()
        except FileNotFoundError:
            print("File not found")
            return

        try:
            self.tableData = json.loads(data)
        except ValueError:
            print("File is corrupted")
            return

        self.refresh_ui()

    def refresh_ui(self):
        if self.tableData:
            self.remove_from_list_button.setEnabled(True)
        else:
            self.remove_from_list_button.setEnabled(False)

        self.tableWidget.cellChanged.disconnect(self.add_to_dict)
        self.tableWidget.setRowCount(len(self.tableData))
        self.tableWidget.clearContents()

        for idx, dict_ in enumerate(self.tableData):
            for type_, data_ in dict_.items():
                self.tableWidget.setItem(idx, int(type_), QTableWidgetItem(data_))

        self.tableWidget.cellChanged.connect(self.add_to_dict)

    def pwd_dict(self):
        data = self.pwd_out.text()
        dict_pwd = {"2": data}
        self.tableData.append(dict_pwd)

        self.write_to_json()

        print(self.tableData)

    def add_to_dict(self):
        current_row = self.tableWidget.currentRow()
        current_column = self.tableWidget.currentColumn()
        self.tableData[current_row][str(current_column)] = self.tableWidget.currentItem().text()

        self.write_to_json()

        print(self.tableData)

    def remove_from_dict(self):
        current_row = self.tableWidget.currentRow()
        del self.tableData[current_row]

        self.write_to_json()

        print(self.tableData)

    def write_to_json(self):
        json_ = json.dumps(self.tableData)
        crypt.encrypt_(json_)

        self.refresh_ui()

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

        generated_pwd = passgen.generate_password(
            pwd_length=self.length_box.value(),
            character=self.get_character())
        self.pwd_out.setText(generated_pwd)

        self.copy_button.setEnabled(True)
        self.add_to_list_button.setEnabled(True)

    def pwd_show(self):
        current_row = self.tableWidget.currentRow()
        self.pwd_out.setText(self.tableData[current_row]["2"])
        self.add_to_list_button.setEnabled(True)
        self.copy_button.setEnabled(True)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        QApplication.clipboard().clear()


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

if __name__ == "__main__":
    app = QApplication([])

    main_widget = MainWidget()

    main_widget.show()

    sys.exit(app.exec())
