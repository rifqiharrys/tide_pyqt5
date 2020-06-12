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




class MergeData(QWidget):

	def __init__(self):
		super(MergeData, self).__init__()

		self.initUI()


	def initUI(self):

		# self.setGeometry(300, 100, 480, 640)
		self.resize(480, 640)
		self.setWindowTitle('Merge Data GUI')
		self.setWindowIcon(QIcon('wave-pngrepo-com.png'))


def entry():

	global merge
	merge = MergeData()
	merge.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	entry()
	# merge = ValeportConvert()
	# merge.show()
	sys.exit(app.exec_())
