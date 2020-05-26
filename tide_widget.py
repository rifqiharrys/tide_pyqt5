#!/usr/bin/python3

import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTextBrowser, QLineEdit, QFileDialog, QAction,
							 QFormLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QRadioButton, 
							 QPushButton, QCalendarWidget)
from PyQt5.QtGui import QIcon
from tdr_py.vp_tide import v_merge, v_dirmerge
import pandas as pd
import numpy as np
from ttide import t_tide, t_utils
from utide import solve, reconstruct
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()



class TideWidget(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()


	def initUI(self):

		self.setGeometry(300, 100, 480, 640)
		self.setWindowTitle('Tide')
		self.setWindowIcon(QIcon('wave-pngrepo-com.png'))

		fileLocButton = QPushButton('Open File Location')
		fileLocButton.clicked.connect(self.pathDialog)
		plotObsButton = QPushButton('Plot Observation Data')
		plotObsButton.clicked.connect(self.plotLoad)
		locLabel = QLabel()
		locLabel.setText('Insert file location:')
		self.locLineForm = QLineEdit()

		timeHeaderLabel = QLabel()
		timeHeaderLabel.setText('Time Header:')
		self.timeHeaderLineForm = QLineEdit()

		depthHeaderLabel = QLabel()
		depthHeaderLabel.setText('Depth Header:')
		self.depthHeaderLineForm = QLineEdit()

		dayFirstLabel = QLabel()
		dayFirstLabel.setText('Day First:')
		self.dayFirstCB = QComboBox()
		self.dayFirstCB.addItems(['True', 'False'])
		# self.dayFirstCB.currentIndexChanged.connect(self.selectionchange)

		sepLabel = QLabel()
		sepLabel.setText('Separator:')
		self.sepCB = QComboBox()
		self.sepCB.addItems(['Tab', 'Space', 'Semicolon'])

		self.dataFrame = QTextBrowser()
		vploadButton = QPushButton('Load Valeport Data')
		plotButton = QPushButton('Plot Loaded Data')

		tideAnalysisLabel = QLabel()
		tideAnalysisLabel.setText('Tidal Analysis Method')
		tideAnalysisLabel.setAlignment(Qt.AlignCenter)
		self.ttideButton = QRadioButton('T Tide')
		# self.ttideButton.toggled.connect()
		self.utideButton = QRadioButton('U Tide')
		# self.utideButton.toggled.connect()

		startcalLabel = QLabel()
		startcalLabel.setText('Start Date')
		startcalLabel.setAlignment(Qt.AlignHCenter)
		startcal = QCalendarWidget()

		endcalLabel = QLabel()
		endcalLabel.setText('End Date')
		endcalLabel.setAlignment(Qt.AlignHCenter)
		endcal = QCalendarWidget()

		# plotButton.clicked.connect(self.plotLoad(dfRaw))



		aboutButton = QPushButton('About')

		# grid = QGridLayout()

		form = QFormLayout()
		vbox = QVBoxLayout()
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox3 = QHBoxLayout()
		hbox4 = QHBoxLayout()

		hbox1.addWidget(fileLocButton)
		hbox1.addWidget(plotObsButton)
		vbox.addLayout(hbox1)

		form.addRow(locLabel, self.locLineForm)
		form.addRow(timeHeaderLabel, self.timeHeaderLineForm)
		form.addRow(depthHeaderLabel, self.depthHeaderLineForm)
		form.addRow(dayFirstLabel, self.dayFirstCB)
		form.addRow(sepLabel, self.sepCB)
		vbox.addLayout(form)

		vbox.addWidget(self.dataFrame)

		vbox.addWidget(tideAnalysisLabel)
		hbox2.addWidget(self.ttideButton)
		hbox2.addWidget(self.utideButton)
		vbox.addLayout(hbox2)

		# startcal.setGridVisible(True)
		hbox3.addWidget(startcalLabel)
		hbox3.addWidget(endcalLabel)
		vbox.addLayout(hbox3)

		hbox4.addWidget(startcal)
		hbox4.addWidget(endcal)
		vbox.addLayout(hbox4)


		vbox.addWidget(vploadButton)
		vbox.addWidget(plotButton)
		vbox.addStretch(1)
		vbox.addWidget(aboutButton)
		# self.setLayout(form)
		self.setLayout(vbox)


	def pathDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Load file', home_dir)
		filePath = str(Path(fname[0]))
		self.locLineForm.setText(filePath)
		# raw = self.convertLoad(filePath)

		if fname[0]:
			f = open(fname[0], 'r')

			with f:
				data = f.read()
				self.dataFrame.setText(data)

		# raw = pd.read_csv(data, sep='\t', index_col='Time')
		# raw.index = pd.to_datetime(raw.index, dayfirst=True)

		# return raw


	def str2bool(self, v):
		return v in ('True')


	def plotLoad(self):

		location = self.locLineForm.text()
		time = self.timeHeaderLineForm.text()
		depth = self.depthHeaderLineForm.text()
		dayF = self.str2bool(self.dayFirstCB.currentText())
		sepDict = {'Tab':'\t', 'Space':' ', 'Semicolon':';'}
		sepSelect = sepDict[self.sepCB.currentText()]

		raw = pd.read_csv(location, sep=sepSelect, index_col=time)
		raw.index = pd.to_datetime(raw.index, dayfirst=dayF)

		ad = raw[depth].values
		at = raw.index

		plt.figure(figsize=(10, 5))
		plt.plot(at, ad, label='Data Pasang Surut Sampel')
		plt.xlabel('Waktu')
		plt.ylabel('Ketinggian Muka Air dari Sensor (m)')
		plt.legend(loc='best')
		plt.show()
	
	# def methodSelect(self, button):
	# 	if button.text == 'T Tide':


	# def dayFirst(self, i):

	# 	for count in range (self.dayFirstCB.count()):



# class TideAnalysis():


# 	def _init_(self):




def main():

	app = QApplication(sys.argv)
	tide = TideWidget()
	tide.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
