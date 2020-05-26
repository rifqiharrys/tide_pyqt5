#!/usr/bin/python3

import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTextBrowser, QLineEdit, QFileDialog, QAction, QFormLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton)
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
		locLabel.setAlignment(Qt.AlignLeft)
		self.locLineForm = QLineEdit()

		timeHeaderLabel = QLabel()
		timeHeaderLabel.setText('Time Header:')
		timeHeaderLabel.setAlignment(Qt.AlignLeft)
		self.timeHeaderLineForm = QLineEdit()

		depthHeaderLabel = QLabel()
		depthHeaderLabel.setText('Depth Header:')
		depthHeaderLabel.setAlignment(Qt.AlignLeft)
		self.depthHeaderLineForm = QLineEdit()

		dayFirstLabel = QLabel()
		dayFirstLabel.setText('Day First:')
		dayFirstLabel.setAlignment(Qt.AlignLeft)
		self.dayFirstCB = QComboBox()
		self.dayFirstCB.addItems(['True', 'False'])
		# self.dayFirstCB.currentIndexChanged.connect(self.selectionchange)

		self.dataFrame = QTextBrowser()
		vploadButton = QPushButton('Load Valeport Data')
		plotButton = QPushButton('Plot Loaded Data')
		# plotButton.clicked.connect(self.plotLoad(dfRaw))



		aboutButton = QPushButton('About')

		# grid = QGridLayout()

		form = QFormLayout()
		vbox = QVBoxLayout()
		hbox1 = QHBoxLayout()

		hbox1.addWidget(fileLocButton)
		hbox1.addWidget(plotObsButton)
		vbox.addLayout(hbox1)

		form.addRow(locLabel, self.locLineForm)
		form.addRow(timeHeaderLabel, self.timeHeaderLineForm)
		form.addRow(depthHeaderLabel, self.depthHeaderLineForm)
		form.addRow(dayFirstLabel, self.dayFirstCB)
		vbox.addLayout(form)

		vbox.addWidget(self.dataFrame)
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

		raw = pd.read_csv(location, sep='\t', index_col=time)
		raw.index = pd.to_datetime(raw.index, dayfirst=dayF)

		ad = raw[depth].values
		at = raw.index

		plt.figure(figsize=(10, 5))
		plt.plot(at, ad, label='Data Pasang Surut Sampel')
		plt.xlabel('Waktu')
		plt.ylabel('Ketinggian Muka Air dari Sensor (m)')
		plt.legend(loc='best')
		plt.show()

	# def dayFirst(self, i):

	# 	for count in range (self.dayFirstCB.count()):



# class TT():

# 	def _init_(self):




def main():

	app = QApplication(sys.argv)
	tide = TideWidget()
	tide.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
