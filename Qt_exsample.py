import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QPushButton, QSlider, QProgressBar, QCalendarWidget
from PyQt5.QtCore import Qt, QDate


def showDate(date):

    print(date.toString())


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.pbar = None
        self.initUI()

    def initUI(self):

        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 80, 200, 25)

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 200)
        cal.clicked[QDate].connect(showDate)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Qt widgets')
        self.show()

    def changeTitle(self, state):

        if state == Qt.Checked:
            self.setWindowTitle('Qt widgets')
        else:
            self.setWindowTitle('')

    def changeValue(self, value):

        self.pbar.setValue(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
