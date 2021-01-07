import mainWindow
import console
from PyQt5 import QtCore, QtGui, QtWidgets


class Program:
    def __init__(self, pui:mainWindow.Ui_MainWindow, pwindow:QtWidgets.QMainWindow):
        self.window = pwindow
        self.ui = pui
        self.console = console
        self.console.output = self.printOutput
        self.console.input = self.reqInput
        self.input:QtWidgets.QLineEdit = pui.consoleInput
        self.output:QtWidgets.QPlainTextEdit = pui.consoleOutput

    def start(self):
        self.window.show()
        self.console.start()

    def printOutput(self, value, *args):
        self.output.appendPlainText(value + (str(args) if len(args) != 0 else "") + "\n")

    def reqInput(self, val):
        if val == None:
            self.input.clear()
            Waiter().wait(self.input.returnPressed, 150000)
            retVal = self.input.text()
            self.printOutput(">> Input: " + retVal)
            return retVal
        self.printOutput(val)
        Waiter().wait(self.input.returnPressed, 150000)
        retVal = self.input.text()
        self.printOutput(">> Input: " + retVal)
        self.input.clear()
        return retVal

class Waiter(QtCore.QObject):
    def __init__(self):
        super(Waiter, self).__init__()
        self.timeout = False
        self.timerID = None
        self.signal_received = False

    def anyslot(self, *args, **kargs):
        print("signal received")
        self.signal_received = True
        self.killTimer(self.timerID)

    def wait(self, signal, timeout):
        signal.connect(self.anyslot)
        self.timerID = self.startTimer(timeout)
        print("Processing loop")
        while not self.timeout and not self.signal_received:
            QtCore.QCoreApplication.instance().processEvents(QtCore.QEventLoop.WaitForMoreEvents) 
        print("Loop done")
        signal.disconnect(self.anyslot)
        return self.signal_received


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)
    program = Program(ui, MainWindow)
    program.start()
    sys.exit(app.exec_())