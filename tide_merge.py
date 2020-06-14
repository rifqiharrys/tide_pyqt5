#!/usr/bin/python3

import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTextBrowser, QLineEdit, QFileDialog, QDialog,
							 QGridLayout, QMessageBox, QVBoxLayout, QComboBox, QLabel, QPushButton,
							 QDoubleSpinBox, QSpinBox)
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

		fileLocButton = QPushButton('Open Folder Location')
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

		indexLabel = QLabel('Index Name:')
		self.indexLineForm = QLineEdit()

		sepLabel = QLabel('Separator:')
		self.sepCB = QComboBox()
		self.sepCB.addItems(['Tab', 'Comma', 'Space', 'Semicolon'])

		saveLocButton = QPushButton('Save File Location')
		saveLocButton.clicked.connect(self.savePathDialog)
		self.saveLocLineForm = QLineEdit()

		startButton =  QPushButton('Start Merge')
		startButton.clicked.connect(self.startMerge)

		self.dataFrame = QTextBrowser()

		grid = QGridLayout()
		vbox = QVBoxLayout()

		grid.addWidget(fileLocButton, 1, 1, 1, 1)
		grid.addWidget(self.locLineForm, 1, 2, 1, 3)

		grid.addWidget(headerLineLabel, 2, 1, 1, 1)
		grid.addWidget(self.headerLineSB, 2, 2, 1, 1)
		grid.addWidget(dataLineLabel, 2, 3, 1, 1)
		grid.addWidget(self.dataLineSB, 2, 4, 1, 1)

		grid.addWidget(sepLabel, 3, 1, 1, 1)
		grid.addWidget(self.sepCB, 3, 2, 1, 1)
		grid.addWidget(indexLabel, 3, 3, 1, 1)
		grid.addWidget(self.indexLineForm, 3, 4, 1, 1)

		grid.addWidget(saveLocButton, 4, 1, 1, 1)
		grid.addWidget(self.saveLocLineForm, 4, 2, 1, 2)
		grid.addWidget(startButton, 4, 4, 1, 1)

		grid.addWidget(self.dataFrame, 5, 1, 4, 4)

		vbox.addStretch(1)
		grid.addLayout(vbox, 20, 1)
		self.setLayout(grid)


	def inputPathDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getExistingDirectory(self, 'Load file', home_dir)
		self.locLineForm.setText(fname)


	def savePathDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getSaveFileName(self, 'Save File', home_dir, 'Text files (*.txt)')
		filePath = (str(Path(fname[0])))
		self.saveLocLineForm.setText(filePath)


	def inputDict(self):

		directory = self.locLineForm.text()
		head = self.headerLineSB.value() - 1
		start_data = self.dataLineSB.value() - 1
		sepDict = {'Tab': '\t', 'Comma': ',', 'Space': ' ', 'Semicolon': ';'}
		sepSelect = sepDict[self.sepCB.currentText()]
		index = self.indexLineForm.text()
		save_file = self.saveLocLineForm.text()

		input_dict = {'dir':directory, 'head':head, 'start':start_data, 'separator':sepSelect, 'index':index, 'save':save_file}

		return input_dict


	def merge(self):

		input_dict = self.inputDict()
		files = input_dict['dir'] + '/**/*.[Tt][Xx][Tt]'
		txtlist = glob.glob(files, recursive=True)

		dummy = []

		for txt in txtlist:
			raw = pd.read_csv(txt, sep=input_dict['separator'], header=input_dict['head'], index_col=input_dict['index'])
			raw = raw.iloc[input_dict['start']:, 0:]

			dummy.append(raw)
		
		merged = pd.concat(dummy, sort=True)

		return merged.sort_index()


	def startMerge(self):

		input_dict = self.inputDict()
		save_file = input_dict['save']
		merged = self.merge()

		merged.to_csv(save_file, sep='\t')

		if save_file:
			f = open(save_file, 'r')

			with f:
				data = f.read()
				self.dataFrame.setText(data)




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
