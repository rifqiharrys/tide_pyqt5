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

		fileLocButton = QPushButton('Open File Location')
		fileLocButton.clicked.connect(self.inputPathDialog)
		# plotObsButton = QPushButton('Plot Observation Data')
		# plotObsButton.clicked.connect(self.plotLoad)
		self.locLineForm = QLineEdit()

		headerLineLabel = QLabel('Header Starting Line:')
		self.headerLineSB = QSpinBox()
		self.headerLineSB.setMinimum(1)

		dataLineLabel = QLabel('Data Starting Line:')
		self.dataLineSB = QSpinBox()
		self.dataLineSB.setMinimum(1)

		timeHeaderLabel = QLabel('Time Header:')
		self.timeHeaderLineForm = QLineEdit()

		depthHeaderLabel = QLabel('Depth Header:')
		self.depthHeaderLineForm = QLineEdit()

		dayFirstLabel = QLabel('Day First:')
		self.dayFirstCB = QComboBox()
		self.dayFirstCB.addItems(['True', 'False'])

		sepLabel = QLabel('Separator:')
		self.sepCB = QComboBox()
		self.sepCB.addItems(['Tab', 'Comma', 'Space', 'Semicolon'])

		saveLocButton = QPushButton('Save File Location')
		saveLocButton.clicked.connect(self.savePathDialog)
		self.saveLocLineForm = QLineEdit()

		self.dataFrame = QTextBrowser()

		grid = QGridLayout()
		vbox = QVBoxLayout()

		grid.addWidget(fileLocButton, 1, 1, 1, 1)
		grid.addWidget(self.locLineForm, 1, 2, 1, 3)

		grid.addWidget(headerLineLabel, 2, 1, 1, 1)
		grid.addWidget(self.headerLineSB, 2, 2, 1, 1)
		grid.addWidget(dataLineLabel, 2, 3, 1, 1)
		grid.addWidget(self.dataLineSB, 2, 4, 1, 1)

		grid.addWidget(timeHeaderLabel, 3, 1, 1, 1)
		grid.addWidget(self.timeHeaderLineForm, 3, 2, 1, 1)
		grid.addWidget(depthHeaderLabel, 3, 3, 1, 1)
		grid.addWidget(self.depthHeaderLineForm, 3, 4, 1, 1)

		grid.addWidget(dayFirstLabel, 4, 1, 1, 1)
		grid.addWidget(self.dayFirstCB, 4, 2, 1, 1)
		grid.addWidget(sepLabel, 4, 3, 1, 1)
		grid.addWidget(self.sepCB, 4, 4, 1, 1)

		grid.addWidget(saveLocButton, 5, 1, 1, 1)
		grid.addWidget(self.saveLocLineForm, 5, 2, 1, 3)

		grid.addWidget(self.dataFrame, 6, 1, 4, 4)

		vbox.addStretch(1)
		grid.addLayout(vbox, 20, 1)
		self.setLayout(grid)


	def inputPathDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getOpenFileNames(self, 'Load file', home_dir)
		fnames = fname[0]
		fnames_str = ''
		for l in range(len(fnames)):
			fnames_str += fnames[l] + '\n'

		print(fnames_str)
		# filePath = str(Path(fname[0]))
		# self.locLineForm.setText(filePath)


	def savePathDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getSaveFileName(self, 'Save File', home_dir, 'Text files (*.txt)')
		filePath = (str(Path(fname[0])))
		self.saveLocLineForm.setText(filePath)



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
