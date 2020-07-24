import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap



# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):
    @pyqtSlot()
    def on_grammar_click(self):
        file = self.grammar_line.text()
        command = 'java -jar ./antlr-4.8-complete.jar -Dlanguage=Python3 -o gen -visitor ' + file
        os.system(command)
        self.grammar_success.setText('...Done')
        self.grammar_success.setStyleSheet("color: green;")
        self.grammar_success.show()

    def on_file_click(self):
        file = self.filetest_line.text()
        command = ' py ./antlerino.py ' + file + ' >output.txt'
        os.system(command)
        self.file_success.setText('...Done')
        self.file_success.setStyleSheet("color: green;")
        self.file_success.show()

    def on_tree_click(self):
        file = open('output.txt').read()
        self.text_tree.setText('Tree: \n' +file)
        self.text_tree.show()
        command = 'py ./graphconverter.py'
        os.system(command)
        #os.system('grun Decaf program -gui')

    def on_java_click(self):
        command = 'py ./javacreate.py'
        os.system(command)

    def on_help_click(self):
        command = 'help.txt'
        os.system(command)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Antlr App")
        self.setFixedSize(1200, 800)
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Enter grammar file:')
        self.nameLabel.setStyleSheet('color: white')
        #label for sucess or error generating files for grammar
        self.grammar_success = QLabel(self)
        self.grammar_success.setText('test')
        self.grammar_success.hide()
        self.grammar_success.move(470, 20)
        ###
        self.grammar_line = QLineEdit(self)
        self.grammar_line.move(130, 20)
        self.grammar_line.resize(200, 32)
        self.grammar_line.setStyleSheet('color:white')
        self.nameLabel.move(20, 20)
        button = QPushButton('Submit', self)
        #button.setToolTip('Submit')
        button.setStyleSheet('color: white; background-color: red;')
        button.move(350,22)
        button.clicked.connect(self.on_grammar_click)

        ##this part is for running the python file
        self.filerunLabel = QLabel(self)
        self.filerunLabel.setText('Enter test file:')
        self.filerunLabel.setStyleSheet('color: white')
        self.filerunLabel.move(20, 80)
        self.filetest_line = QLineEdit(self)
        self.filetest_line.move(130, 80)
        self.filetest_line.resize(200, 32)
        self.filetest_line.setStyleSheet('color:white')
        button_file = QPushButton('Submit', self)
        # button.setToolTip('Submit')
        button_file.setStyleSheet('color: white; background-color: red;')
        button_file.move(350, 82)
        button_file.clicked.connect(self.on_file_click)
        self.file_success = QLabel(self)
        self.file_success.setText('test')
        self.file_success.hide()
        self.file_success.move(470, 80)
        ##show tree
        button_tree = QPushButton('Display tree', self)
        button_tree.setStyleSheet('color: white; background-color: red;')
        button_tree.move(20, 140)
        button_tree.clicked.connect(self.on_tree_click)
        self.text_tree = QLabel(self)
        self.text_tree.setText('Tree')
        self.text_tree.hide()
        self.text_tree.setStyleSheet('color: white')
        self.text_tree.resize(200, 230)
        self.text_tree.move(20, 190)
        #doge
        self.dogeImage = QLabel(self)
        pixmap = QPixmap("doge.jpg")
        self.dogeImage.setPixmap(pixmap)
        self.dogeImage.move(300, 300)
        self.dogeImage.resize(793, 415)
        #java button
        button_java = QPushButton('Java', self)
        button_java.setStyleSheet('color: white; background-color: red;')
        button_java.move(1050, 22)
        button_java.clicked.connect(self.on_java_click)
        #help button
        button_help = QPushButton('Help', self)
        button_help.setStyleSheet('color: white; background-color: red;')
        button_help.move(1050, 62)
        button_help.clicked.connect(self.on_help_click)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
