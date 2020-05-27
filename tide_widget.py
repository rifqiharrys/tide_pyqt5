#!/usr/bin/python3

import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTextBrowser, QLineEdit, QFileDialog, QAction,
							 QGridLayout, QFormLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel,
                             QRadioButton, QPushButton, QCalendarWidget, QDoubleSpinBox)
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
		fileLocButton.clicked.connect(self.inputPathDialog)
		plotObsButton = QPushButton('Plot Observation Data')
		plotObsButton.clicked.connect(self.plotLoad)
		locLabel = QLabel('Insert file location:')
		self.locLineForm = QLineEdit()

		timeHeaderLabel = QLabel('Time Header:')
		self.timeHeaderLineForm = QLineEdit()

		depthHeaderLabel = QLabel('Depth Header:')
		self.depthHeaderLineForm = QLineEdit()

		dayFirstLabel = QLabel('Day First:')
		self.dayFirstCB = QComboBox()
		self.dayFirstCB.addItems(['True', 'False'])
		# self.dayFirstCB.currentIndexChanged.connect(self.selectionchange)

		sepLabel = QLabel('Separator:')
		self.sepCB = QComboBox()
		self.sepCB.addItems(['Tab', 'Space', 'Semicolon'])

		self.dataFrame = QTextBrowser()
		vploadButton = QPushButton('Load Valeport Data')
		plotButton = QPushButton('Plot Loaded Data')

		self.methodLabel = QLabel()
		self.methodLabel.setAlignment(Qt.AlignRight)
		tideAnalysisLabel = QLabel()
		tideAnalysisLabel.setText('Tidal Analysis Method')
		tideAnalysisLabel.setAlignment(Qt.AlignLeft)
		self.ttideButton = QRadioButton('T Tide')
		self.ttideButton.toggled.connect(self.methodButton)
		self.utideButton = QRadioButton('U Tide')
		self.utideButton.toggled.connect(self.methodButton)

		latLabel = QLabel('Latitude (dd.ddddd):')
		self.latDSB = QDoubleSpinBox()
		self.latDSB.setRange(-90.0, 90.0)
		self.latDSB.setDecimals(5)

		self.saveLocForm = QLineEdit()
		saveLocButton = QPushButton('Save File Location')

		startcalLabel = QLabel('Start Date')
		startcalLabel.setAlignment(Qt.AlignHCenter)
		self.startcal = QCalendarWidget()

		endcalLabel = QLabel('End Date')
		endcalLabel.setAlignment(Qt.AlignHCenter)
		self.endcal = QCalendarWidget()

		solveButton = QPushButton('Analyse Tide')
		solveButton.clicked.connect(self.analyseButton)
		predicButton = QPushButton('Predict Tide')


		# plotButton.clicked.connect(self.plotLoad(dfRaw))



		aboutButton = QPushButton('About')

		grid = QGridLayout()
		vbox = QVBoxLayout()
		
		grid.addWidget(fileLocButton, 1, 1, 1, 1)
		grid.addWidget(self.locLineForm, 1, 2, 1, 2)
		grid.addWidget(plotObsButton, 1, 4, 1, 1)
		grid.addWidget(timeHeaderLabel, 2, 1, 1, 1)
		grid.addWidget(self.timeHeaderLineForm, 2, 2, 1, 1)
		grid.addWidget(depthHeaderLabel, 2, 3, 1, 1)
		grid.addWidget(self.depthHeaderLineForm, 2, 4, 1, 1)
		grid.addWidget(dayFirstLabel, 3, 1, 1, 1)
		grid.addWidget(self.dayFirstCB, 3, 2, 1, 1)
		grid.addWidget(sepLabel, 3, 3, 1, 1)
		grid.addWidget(self.sepCB, 3, 4, 1, 1)
		grid.addWidget(self.dataFrame, 4, 1, 4, 4)
		grid.addWidget(self.methodLabel, 8, 1, 1, 2)
		grid.addWidget(tideAnalysisLabel, 8, 3, 1, 2)
		grid.addWidget(self.ttideButton, 9, 1, 1, 2)
		grid.addWidget(self.utideButton, 9, 3, 1, 2)
		grid.addWidget(latLabel, 10, 1, 1, 1)
		grid.addWidget(self.latDSB, 10, 2, 1, 1)
		grid.addWidget(self.saveLocForm, 10, 3, 1, 1)
		grid.addWidget(saveLocButton, 10, 4, 1, 1)
		grid.addWidget(startcalLabel, 11, 1, 1, 2)
		grid.addWidget(endcalLabel, 11, 3, 1, 2)
		grid.addWidget(self.startcal, 12, 1, 1, 2)
		grid.addWidget(self.endcal, 12, 3, 1, 2)
		grid.addWidget(solveButton, 13, 1, 1, 2)
		grid.addWidget(predicButton, 13, 3, 1, 2)


		vbox.addStretch(1)
		grid.addLayout(vbox, 20, 1)
		self.setLayout(grid)

		# form = QFormLayout()
		# vbox = QVBoxLayout()
		# hbox1 = QHBoxLayout()
		# hbox2 = QHBoxLayout()
		# hbox3 = QHBoxLayout()
		# hbox4 = QHBoxLayout()
		# hbox5 = QHBoxLayout()

		# hbox1.addWidget(fileLocButton)
		# hbox1.addWidget(plotObsButton)
		# vbox.addLayout(hbox1)

		# form.addRow(locLabel, self.locLineForm)
		# form.addRow(timeHeaderLabel, self.timeHeaderLineForm)
		# form.addRow(depthHeaderLabel, self.depthHeaderLineForm)
		# # form.addRow(dayFirstLabel, self.dayFirstCB)
		# # form.addRow(sepLabel, self.sepCB)
		# vbox.addLayout(form)
		# hbox5.addWidget(dayFirstLabel)
		# hbox5.addWidget(self.dayFirstCB)
		# hbox5.addWidget(sepLabel)
		# hbox5.addWidget(self.sepCB)
		# vbox.addLayout(hbox5)

		# vbox.addWidget(self.dataFrame)

		# vbox.addWidget(tideAnalysisLabel)
		# hbox2.addWidget(self.ttideButton)
		# hbox2.addWidget(self.utideButton)
		# vbox.addLayout(hbox2)

		# # startcal.setGridVisible(True)
		# hbox3.addWidget(startcalLabel)
		# hbox3.addWidget(endcalLabel)
		# vbox.addLayout(hbox3)

		# hbox4.addWidget(self.startcal)
		# hbox4.addWidget(self.endcal)
		# vbox.addLayout(hbox4)


		# vbox.addWidget(vploadButton)
		# vbox.addWidget(plotButton)
		# vbox.addStretch(1)
		# vbox.addWidget(aboutButton)
		# # self.setLayout(form)
		# self.setLayout(vbox)


	def inputPathDialog(self):

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

	def inputDict(self):

		location = self.locLineForm.text()
		time = self.timeHeaderLineForm.text()
		depth = self.depthHeaderLineForm.text()
		dayF = self.str2bool(self.dayFirstCB.currentText())
		sepDict = {'Tab':'\t', 'Space':' ', 'Semicolon':';'}
		sepSelect = sepDict[self.sepCB.currentText()]

		raw = pd.read_csv(location, sep=sepSelect, index_col=time)
		raw.index = pd.to_datetime(raw.index, dayfirst=dayF)

		depth_array = raw[depth].values
		time_array = raw.index

		startcal_string = self.startcal.selectedDate().toString(Qt.ISODate)
		endcal_string = self.endcal.selectedDate().toString(Qt.ISODate)
		# start_string = start.toString(Qt.ISODate)

		input_dict = {'depth':depth_array, 'time':time_array, 'start':startcal_string, 'end':endcal_string}

		return input_dict

	def plotLoad(self):

		input_dict = self.inputDict()

		ad = input_dict['depth']
		at = input_dict['time']

		plt.figure(figsize=(10, 5))
		plt.plot(at, ad, label='Data Pasang Surut Sampel')
		plt.xlabel('Waktu')
		plt.ylabel('Ketinggian Muka Air dari Sensor')
		plt.legend(loc='best')
		plt.show()
	
	def methodButton(self):

		method_button = self.sender()
		if method_button.isChecked():
			self.methodLabel.setText(method_button.text())



	def analyseButton(self):
		method_dict = {'T Tide':self.ttide, 'U Tide':self.utide}
		method = self.methodLabel.text()
		method_dict[method]()

	def ttide(self):

		input_dict = self.inputDict()
		ad = input_dict['depth']
		at = input_dict['time']

		# demeaned_ad = ad - np.nanmean(ad)
		time_num = date2num(at.to_pydatetime())

		# time_predic = pd.date_range(start=, end=, freq=)
		# time_predic_num = date2num(time_predic.to_pydatetime())

		coef = t_tide(ad, dt=1, stime=time_num[0], lat=-2.670602, synth=0)
		predic = coef(time_num) + np.nanmean(ad)

		output_dict = {'coefficient':coef, 'prediction':predic}

		return output_dict

	def utide(self):

		input_dict = self.inputDict()
		ad = input_dict['depth']
		at = input_dict['time']

		# demeaned_ad = ad - np.nanmean(ad)
		time_num = date2num(at.to_pydatetime())

		coef = solve(time_num, ad, lat=-2.670602)
		predic = reconstruct(time_num, coef)

		output_dict = {'coefficient':coef, 'prediction':predic}

		return output_dict

	
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
