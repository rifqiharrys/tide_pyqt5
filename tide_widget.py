#!/usr/bin/python3

import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTextBrowser, QLineEdit, QFileDialog, QDialog,
							 QGridLayout, QMessageBox, QVBoxLayout, QComboBox, QLabel,QRadioButton,
							 QPushButton, QCalendarWidget, QDoubleSpinBox, QSpinBox, QCheckBox,
							 QTableWidget, QScrollArea, QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QIcon
# from tdr_py.vp_tide import v_merge, v_dirmerge
import pandas as pd
import numpy as np
from ttide import t_tide, t_utils
from utide import solve, reconstruct
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import tide_merge
from statistics import mode



class TideWidget(QWidget):

	def __init__(self):
		super(TideWidget, self).__init__()

		self.initUI()


	def mergeData(self):

		tide_merge.main()

	def initUI(self):

		self.setGeometry(300, 100, 480, 640)
		self.setWindowTitle('Tide Analysis and Prediction GUI')
		self.setWindowIcon(QIcon('wave-pngrepo-com.png'))

		fileLocButton = QPushButton('Open File Location')
		fileLocButton.clicked.connect(self.inputPathDialog)
		mergeButton = QPushButton('Merge Data')
		mergeButton.clicked.connect(self.mergeData)
		plotObsButton = QPushButton('Plot Observation Data')
		plotObsButton.clicked.connect(self.plotLoad)
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

		self.dataFrame = QTextBrowser()

		self.methodLabel = QLabel()
		self.methodLabel.setAlignment(Qt.AlignRight)
		tideAnalysisLabel = QLabel()
		tideAnalysisLabel.setText('Tidal Analysis Method')
		tideAnalysisLabel.setAlignment(Qt.AlignLeft)
		self.ttideButton = QRadioButton('T Tide')
		self.ttideButton.toggled.connect(self.methodButton)
		self.ttideButton.setChecked(True)
		self.utideButton = QRadioButton('U Tide')
		self.utideButton.toggled.connect(self.methodButton)

		latLabel = QLabel('Latitude (dd.ddddd):')
		self.latDSB = QDoubleSpinBox()
		self.latDSB.setRange(-90.0, 90.0)
		self.latDSB.setDecimals(6)
		self.latDSB.setValue(0.000001)

		self.saveLocLineForm = QLineEdit()
		saveLocButton = QPushButton('Save File Location')
		saveLocButton.clicked.connect(self.savePathDialog)

		startcalLabel = QLabel('Start Date')
		startcalLabel.setAlignment(Qt.AlignHCenter)
		self.startcal = QCalendarWidget()

		endcalLabel = QLabel('End Date')
		endcalLabel.setAlignment(Qt.AlignHCenter)
		self.endcal = QCalendarWidget()

		freqLabel = QLabel('Time Interval:')
		self.freqSB = QSpinBox()
		self.freqSB.setValue(1)
		self.freqUnitCB = QComboBox()
		self.freqUnitCB.addItems(['hours', 'minutes'])

		solveButton = QPushButton('Analyse Tide')
		solveButton.clicked.connect(self.analyse)
		predicButton = QPushButton('Predict Tide')
		predicButton.clicked.connect(self.predict)

		self.saveCheckBox = QCheckBox('Save Prediction')
		self.saveCheckBox.setChecked(True)
		self.saveCheckBox.toggled.connect(self.checkBox)
		self.saveState = QLabel()

		self.plotCheckBox = QCheckBox('Plot Prediction')
		self.plotCheckBox.setChecked(True)
		self.plotCheckBox.toggled.connect(self.checkBox)
		self.plotState = QLabel()


		howToButton = QPushButton('How To Use')
		howToButton.clicked.connect(self.howToDialog)
		aboutButton = QPushButton('About')
		aboutButton.clicked.connect(self.aboutDialog)

		grid = QGridLayout()
		vbox = QVBoxLayout()
		
		grid.addWidget(fileLocButton, 1, 1, 1, 1)
		grid.addWidget(self.locLineForm, 1, 2, 1, 1)
		grid.addWidget(mergeButton, 1, 3, 1, 1)
		grid.addWidget(plotObsButton, 1, 4, 1, 1)

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

		grid.addWidget(self.dataFrame, 5, 1, 4, 4)

		grid.addWidget(self.methodLabel, 9, 1, 1, 2)
		grid.addWidget(tideAnalysisLabel, 9, 3, 1, 2)

		grid.addWidget(self.ttideButton, 10, 1, 1, 2)
		grid.addWidget(self.utideButton, 10, 3, 1, 2)

		grid.addWidget(latLabel, 11, 1, 1, 1)
		grid.addWidget(self.latDSB, 11, 2, 1, 1)
		grid.addWidget(saveLocButton, 11, 3, 1, 1)
		grid.addWidget(self.saveLocLineForm, 11, 4, 1, 1)

		grid.addWidget(startcalLabel, 12, 1, 1, 2)
		grid.addWidget(endcalLabel, 12, 3, 1, 2)

		grid.addWidget(self.startcal, 13, 1, 1, 2)
		grid.addWidget(self.endcal, 13, 3, 1, 2)

		grid.addWidget(freqLabel, 14, 1, 1, 1)
		grid.addWidget(self.freqSB, 14, 2, 1, 2)
		grid.addWidget(self.freqUnitCB, 14, 4, 1, 1)

		grid.addWidget(self.saveCheckBox, 15, 2, 1, 1)
		grid.addWidget(self.plotCheckBox, 15, 3, 1, 1)
		grid.addWidget(solveButton, 15, 1, 1, 1)
		grid.addWidget(predicButton, 15, 4, 1, 1)


		vbox.addStretch(1)
		grid.addLayout(vbox, 20, 1)
		grid.addWidget(howToButton, 21, 1, 1, 2)
		grid.addWidget(aboutButton, 21, 3, 1, 2)
		self.setLayout(grid)


	def inputPathDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Load file', home_dir)
		filePath = str(Path(fname[0]))
		self.locLineForm.setText(filePath)

		if fname[0]:
			f = open(fname[0], 'r')

			with f:
				data = f.read()
				self.dataFrame.setText(data)


	def savePathDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getSaveFileName(self, 'Save File', home_dir, 'Text files (*.txt)')
		filePath = (str(Path(fname[0])))
		self.saveLocLineForm.setText(filePath)


	def str2bool(self, v):
		
		return v in ('True')


	def inputDict1(self):

		location = self.locLineForm.text()
		head = self.headerLineSB.value() - 1
		start_data = self.dataLineSB.value() - 1
		time = self.timeHeaderLineForm.text()
		depth = self.depthHeaderLineForm.text()
		dayF = self.str2bool(self.dayFirstCB.currentText())
		sepDict = {'Tab':'\t', 'Comma':',', 'Space':' ', 'Semicolon':';'}
		sepSelect = sepDict[self.sepCB.currentText()]

		raw = pd.read_csv(location, sep=sepSelect, index_col=time, header=head)
		raw = raw.iloc[start_data:,0:]
		raw.index = pd.to_datetime(raw.index, dayfirst=dayF)
		raw = raw.sort_index()

		depth_array = raw[depth].values
		time_array = raw.index

		time_diff_list = []

		t_length = len(time_array)
		for i in range(t_length):
			if i < t_length - 1:
				time_diff = np.timedelta64(time_array[i + 1]-time_array[i], 'm').astype('float64') / 60
			else:
				pass

			time_diff_list.append(time_diff)

		time_diff = mode(time_diff_list)

		time_array2 = pd.date_range(start=time_array[0], end=time_array[t_length - 1], freq=str(time_diff)+'H')
		t2_length = len(time_array2)

		dummy = pd.DataFrame(np.nan, index=time_array2, columns=list('a'))

		raw2 = pd.concat([raw, dummy], axis=1)
		depth_array2 = raw2[depth].values

		input_dict = {'depth':depth_array2, 'time':time_array2, 'interval':time_diff}

		return input_dict


	def inputDict2(self):

		startcal_string = self.startcal.selectedDate().toString(Qt.ISODate)
		endcal_string = self.endcal.selectedDate().toString(Qt.ISODate)

		freq_unit_dict = {'hours':'H', 'minutes':'min'}
		freq_unit_value = freq_unit_dict[self.freqUnitCB.currentText()]

		if self.latDSB.value() == 0.0 or self.freqSB.value() == 0:
			self.zeroWarning()
			lat = None
		else:
			lat = self.latDSB.value()
			frequency = str(self.freqSB.value()) + freq_unit_value

		time_predic = pd.date_range(start=startcal_string, end=endcal_string, freq=frequency)

		save_file = self.saveLocLineForm.text()

		input_dict = {'latitude':lat, 'predicted time':time_predic, 'save':save_file}

		return input_dict


	def plotLoad(self):

		input_dict = self.inputDict1()

		ad = input_dict['depth']
		at = input_dict['time']

		plt.figure(figsize=(10, 5))
		plt.plot(at, ad, label='Tide Observation Data')
		plt.xlabel('Time')
		plt.ylabel('Water Level')
		plt.legend(loc='best')
		plt.show()


	def plotPredic(self, water_level):

		input_dict2 = self.inputDict2()

		ad = water_level
		at = input_dict2['predicted time']
		data_label = 'Predicted Data using ' + self.methodLabel.text()

		plt.figure(figsize=(10, 5))
		plt.plot(at, ad, label=data_label)
		plt.xlabel('Time')
		plt.ylabel('Water Level')
		plt.legend(loc='best')
		plt.show()


	def methodButton(self):

		method_button = self.sender()
		if method_button.isChecked():
			self.methodLabel.setText(method_button.text())


	def checkBox(self):

		if self.saveCheckBox.isChecked() == True:
			self.saveState.setText(self.saveCheckBox.text())
		else:
			self.saveState.setText('unchecked')

		if self.plotCheckBox.isChecked() == True:
			self.plotState.setText(self.plotCheckBox.text())
		else:
			self.plotState.setText('unchecked')


	def analyse(self):

		input_dict2 = self.inputDict2()
		save_file = input_dict2['save']

		method_dict = {'T Tide':self.ttideAnalyse, 'U Tide':self.utideAnalyse}
		method = self.methodLabel.text()
		coef = method_dict[method]()

		method = method.replace(' ', '-')
		text_edit = '_' + method + '_report.txt'
		save_file = save_file.replace('.txt', text_edit)

		if method == 'T-Tide':
			print_coef = t_utils.pandas_style(coef)
			report = open(save_file, 'w')
			report.write(print_coef)
		elif method == 'U-Tide':
			print_coef = pd.DataFrame({'name': coef.name, 'frq': coef.aux.frq, 'lind': coef.aux.lind, 
			'A': coef.A, 'g': coef.g, 'A_ci': coef.A_ci, 'g_ci': coef.g_ci, 'PE': coef.diagn['PE'], 
			'SNR': coef.diagn['SNR']})
			print_coef.index = print_coef['name']
			print_coef = print_coef.iloc[:, 1:]
			print_coef.to_csv(save_file, sep='\t')


	def predict(self):

		input_dict2 = self.inputDict2()
		save_file = input_dict2['save']

		method_dict = {'T Tide':self.ttidePredict, 'U Tide':self.utidePredict}
		method = self.methodLabel.text()
		prediction = method_dict[method]()

		time = input_dict2['predicted time']

		if method == 'T Tide':
			water_level = prediction
		elif method == 'U Tide':
			water_level = prediction['h']

		predic_out = pd.DataFrame({'Time':time, 'Depth':water_level})


		if self.saveState.text() == 'Save Prediction':
			method = method.replace(' ', '-')
			text_edit = '_' + method + '.txt'
			save_file = save_file.replace('.txt', text_edit)

			predic_out.index = predic_out['Time']
			predic_out = predic_out.iloc[:, 1:2]
			predic_out.to_csv(save_file, sep='\t')
		else:
			pass

		if self.plotState.text() == 'Plot Prediction':
			self.plotPredic(water_level)
		else:
			pass

		if self.saveState.text() == 'unchecked' and self.plotState.text() == 'unchecked':
			self.showPredicDialog(predic_out)


	def ttideAnalyse(self):

		input_dict1 = self.inputDict1()
		input_dict2 = self.inputDict2()
		ad = input_dict1['depth']
		at = input_dict1['time']
		latitude = input_dict2['latitude']
		time_diff = input_dict1['interval']
		time_num = date2num(at.to_pydatetime())

		time_predic = input_dict2['predicted time']

		coef = t_tide(ad, dt=time_diff, stime=time_num[0], lat=latitude, synth=0)

		return coef


	def ttidePredict(self):

		input_dict1 = self.inputDict1()
		input_dict2 = self.inputDict2()
		ad = input_dict1['depth']

		time_predic = input_dict2['predicted time']
		time_predic_num = date2num(time_predic.to_pydatetime())

		coef = self.ttideAnalyse()
		predic = coef(time_predic_num) + np.nanmean(ad)

		return predic


	def utideAnalyse(self):

		input_dict1 = self.inputDict1()
		input_dict2 = self.inputDict2()
		ad = input_dict1['depth']
		at = input_dict1['time']

		time_num = date2num(at.to_pydatetime())
		latitude = input_dict2['latitude']

		coef = solve(time_num, ad, lat=latitude)

		return coef


	def utidePredict(self):

		input_dict2 = self.inputDict2()

		time_predic = input_dict2['predicted time']
		time_predic_num = date2num(time_predic.to_pydatetime())

		coef = self.utideAnalyse()
		predic = reconstruct(time_predic_num, coef, min_SNR=0)

		return predic


	def zeroWarning(self):

		zeroWarning = QMessageBox()
		zeroWarning.setWindowTitle('Warning')
		zeroWarning.setIcon(QMessageBox.Critical)
		zeroWarning.setText('Cannot process zero value.')

		zeroWarning.exec_()


	def showPredicDialog(self, data):

		showPredic = QDialog()
		showPredic.setWindowTitle('Tide Prediction')
		showPredic.setWindowIcon(QIcon('wave-pngrepo-com.png'))
		showPredic.resize(320, 720)
		closeButton = QPushButton("Close")
		closeButton.clicked.connect(showPredic.close)

		table = QTableWidget()
		header = table.horizontalHeader()
		scroll = QScrollArea()
		grid = QGridLayout()
		scroll.setWidget(table)
		grid.addWidget(table, 1, 1, 25, 4)
		grid.addWidget(closeButton, 26, 4, 1, 1)
		showPredic.setLayout(grid)

		table.setColumnCount(len(data.columns))
		table.setRowCount(len(data.index))

		for h in range(len(data.columns)):
			table.setHorizontalHeaderItem(h, QTableWidgetItem(data.columns[h]))

		for i in range(len(data.index)):
			for j in range(len(data.columns)):
				table.setItem(i, j, QTableWidgetItem(str(data.iloc[i, j])))

		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		showPredic.exec_()


	def howToDialog(self):

		howTo = QDialog()
		howTo.setWindowTitle('How to Use')
		howTo.setWindowIcon(QIcon('wave-pngrepo-com.png'))
		closeButton = QPushButton("Close")
		closeButton.clicked.connect(howTo.close)

		how_to_use = open('how_to_use.txt', 'r')
		howToLabel = QLabel('The details of how to use this tide analysis GUI is as follows:')
		howToTextBrowser = QTextBrowser()
		howToTextBrowser.setText(how_to_use.read())

		grid = QGridLayout()
		grid.addWidget(howToLabel, 1, 1, 1, 4)
		grid.addWidget(howToTextBrowser, 2, 1, 50, 4)
		grid.addWidget(closeButton, 52, 4, 1, 1)
		howTo.setLayout(grid)

		howTo.exec_()


	def aboutDialog(self):

		about = QDialog()
		about.setWindowTitle('About')
		about.setWindowIcon(QIcon('wave-pngrepo-com.png'))
		closeButton = QPushButton("Close")
		closeButton.clicked.connect(about.close)

		aboutText = '''<body>
		This is a tidal analysis GUI using T Tide and U Tide (both Python version).
		<br><\br><br><\br>
		The GUI itself was developed by 
		<a href=\'https://github.com/rifqiharrys/tide_pyqt5'>Rifqi Muhammad Harrys</a> 
		using PyQt5, a python GUI library.
		<br><\br><br><\br>
		Both T Tide and U Tide developed by two different entities.
		<br><\br>
		The original versions of <a href=\'https://www.eoas.ubc.ca/~rich/#T_Tide'>T Tide</a> and 
		<a href=\'https://www.mathworks.com/matlabcentral/fileexchange/46523-utide-unified-tidal-analysis-and-prediction-functions?w.mathworks.com'>U Tide</a> 
		are in MATLAB language developed by R. Pawlowicz et. al (T Tide) and Daniel Codiga (U Tide).<br><\br><br><\br>
		The python version of <a href=\'https://github.com/moflaher/ttide_py'>T Tide</a> and 
		<a href=\'https://github.com/wesleybowman/UTide'>U Tide</a> were developed by moflaher (T Tide) and Wesley Bowman (U Tide).
		<br><\br><br><\br>
		A description of the theoretical basis of the analysis and some implementation details 
		of T Tide and U Tide Matlab version can be found in:
		</body>'''

		tideCite = '''
		<cite>R. Pawlowicz, B. Beardsley, and S. Lentz, 
		"Classical tidal harmonic analysis including error estimates in MATLAB using 
		T_TIDE", Computers and Geosciences 28 (2002), 929-937.</cite>
		<br><\br><br><\br>
		<cite>Codiga, D.L., 2011. Unified Tidal Analysis and Prediction Using the 
		UTide Matlab Functions. Technical Report 2011-01. Graduate School of Oceanography, 
		University of Rhode Island, Narragansett, RI. 59pp.</cite>
		'''

		aboutLabel1 = QLabel(aboutText)
		aboutLabel1.setWordWrap(True)
		aboutLabel1.setOpenExternalLinks(True)
		aboutLabel2 = QLabel(tideCite)
		aboutLabel2.setTextInteractionFlags(Qt.TextSelectableByMouse)
		aboutLabel2.setWordWrap(True)
		aboutTB = QTextBrowser()
		aboutTB.setText(tideCite)
		grid = QGridLayout()
		grid.addWidget(aboutLabel1, 1, 1, 1, 4)
		grid.addWidget(aboutTB, 2, 1, 1, 4)
		grid.addWidget(closeButton, 3, 4, 1, 1)

		about.setLayout(grid)

		about.exec_()



def main():

	global tide
	tide = TideWidget()
	tide.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	main()
	sys.exit(app.exec_())
