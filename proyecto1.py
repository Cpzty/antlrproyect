import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QPlainTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Proyecto 1'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def file_open(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')
        text = open(filename[0]).read()
        self.TextEditor.setPlainText(text)

    def on_submit(self):
        file = open('current.decaf', 'w')
        text = self.TextEditor.toPlainText()
        file.write(text)
        file.close()
        command = ' py ./antlerino.py current.decaf'
        stream = os.popen(command)
        output = stream.readlines()
        msg_outp = ''
        msg_tables = output[-3] + output[-2] + output[-1]
        for i in range(len(output)-3):
            msg_outp = msg_outp + output[i]
        self.ErrorMessages.setText(msg_outp)
        self.TableMessages.setText(msg_tables)


    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Editor")
        self.tabs.addTab(self.tab2, "Mensajes")
        self.tabs.addTab(self.tab3, "Tablas")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)
        self.tab3.layout = QVBoxLayout(self)

        self.tab2.layout.setAlignment(Qt.AlignTop)
        self.tab3.layout.setAlignment(Qt.AlignTop)

        self.TextEditor = QPlainTextEdit(self)
        self.TextEditor.resize(100, 100)
        self.uploadBtn = QPushButton("Upload file")
        self.uploadBtn.clicked.connect(self.file_open)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.move(100, 100)
        self.submitBtn.resize(50,50)
        self.submitBtn.clicked.connect(self.on_submit)

        #Elements for 2nd tab
        self.ErrorMessages = QLabel(self)
        self.TableMessages = QLabel(self)
        #Add to tab1
        self.tab1.layout.addWidget(self.TextEditor)
        self.tab1.layout.addWidget(self.uploadBtn)
        self.tab1.layout.addWidget(self.submitBtn)
        self.tab1.setLayout(self.tab1.layout)

        #Add to tab2
        self.tab2.layout.addWidget(self.ErrorMessages)
        self.tab2.setLayout(self.tab2.layout)

        #Add to tab3
        self.tab3.layout.addWidget(self.TableMessages)
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())