from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtGui
import sys

import MainWindow
import passgen
import options

"""
from subprocess import run

run("pyuic5 -o MainWindow.py Ui.ui", shell=True)
"""


class MainWidget(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.copy_button.setEnabled(False)
        self.generate_button.clicked.connect(self.generate_onclick)
        self.copy_button.clicked.connect(self.copy_onclick)

    def generate_onclick(self):
        self.set_password()

    def copy_onclick(self):
        QtGui.QGuiApplication.clipboard().setText(self.pwd_out.text())

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
            return

        if not self.get_character():
            self.pwd_out.setText("Choose at least one option")
            self.copy_button.setEnabled(False)
            return

        try:
            self.pwd_out.setText(
                passgen.generate_password(
                    pwd_length=self.length_box.value(),
                    character=self.get_character()
                )
            )
            self.copy_button.setEnabled(True)

        except IndexError:
            self.pwd_out.clear()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        QApplication.clipboard().clear()


if __name__ == "__main__":
    app = QApplication([])

    main_widget = MainWidget()

    main_widget.show()

    sys.exit(app.exec())
