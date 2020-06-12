#!/usr/bin/python3

import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTextBrowser, QLineEdit, QFileDialog, QDialog,
							 QGridLayout, QFormLayout, QMessageBox, QVBoxLayout, QComboBox, QLabel,
							 QRadioButton, QPushButton, QCalendarWidget, QDoubleSpinBox, QSpinBox,
							 QCheckBox, QTableWidget, QScrollArea, QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QIcon
import pandas as pd
import glob
import os




class ValeportConvert(QWidget):

	def __init__(self):
		super(ValeportConvert, self).__init__()

		self.initUI()


	def initUI(self):

		self.setGeometry(300, 100, 480, 640)
		self.setWindowTitle('Valeport Data Conversion GUI')
		self.setWindowIcon(QIcon('wave-pngrepo-com.png'))


def main():

	app = QApplication(sys.argv)
	vp = ValeportConvert()
	vp.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
