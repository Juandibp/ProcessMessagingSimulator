import mainWindow
import console
from PyQt5 import QtCore, QtGui, QtWidgets


class Program:
    def __init__(self, pui:mainWindow.Ui_MainWindow, pwindow:QtWidgets.QMainWindow):
        self.window = pwindow
        self.ui = pui
        self.input:QtWidgets.QLineEdit = pui.consoleInput
        self.output:QtWidgets.QPlainTextEdit = pui.consoleOutput
        self.input.returnPressed.connect(self.retPressed)
    
    def retPressed(self):
        print("return was pressed")

    def start(self):
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)
    program = Program(ui, MainWindow)
    program.start()
    sys.exit(app.exec_())