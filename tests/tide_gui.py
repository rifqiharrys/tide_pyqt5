#!/usr/bin/python3

"""
ZetCode PyQt5 tutorial

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QTextEdit, QFileDialog, QAction, QMenu, QHBoxLayout, QVBoxLayout, QFrame, QSplitter, QMessageBox, qApp)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from tdr_py.vp_tide import v_merge, v_dirmerge
import pandas as pd
import numpy as np
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class TideMain(QMainWindow):

	def __init__(self):
		super().__init__()

		self.initUI()


	def initUI(self):

		self.statusBar().showMessage('Ready')

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('File')
		toolsMenu = menubar.addMenu('Tools')

		loadFile = QAction(QIcon('load-pngrepo-com.png'), 'Load File', self)
		loadFile.setShortcut('Ctrl+O')
		loadFile.setStatusTip('Load file')
		loadFile.triggered.connect(self.loadDialog)

		exitFile = QAction(QIcon('exit-pngrepo-com.png'), 'Exit', self)
		exitFile.setShortcut('Ctrl+Q')
		exitFile.setStatusTip('Exit application')
		# exitFile.triggered.connect(self.close)
		exitFile.triggered.connect(self.close)

		fileMenu.addAction(loadFile)
		fileMenu.addAction(exitFile)

		vpTools = QMenu('Valeport Data', self)
		vpmergeAct = QAction('Merge', self)
		vpmergeAct.setStatusTip('Merge valeport based files inside a directory')
		vpTools.addAction(vpmergeAct)

		toolsMenu.addMenu(vpTools)

		self.loadToolbar = self.addToolBar('Load File')
		self.loadToolbar.addAction(loadFile)

		self.show()

		self.loadFrame = QTextEdit(QFrame(self))
		self.loadFrame.setFrameShape(QFrame.StyledPanel)

		self.setCentralWidget(self.loadFrame)
		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle('Tide')
		self.setWindowIcon(QIcon('wave-pngrepo-com.png'))
		# self.textEdit = QTextEdit()
		# self.setCentralWidget(self.textEdit)


	def loadDialog(self):

		home_dir = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Load file', home_dir)

		if fname[0]:
			f = open(fname[0], 'r')

			with f:
				data = f.read()

				self.loadFrame.setText(data)

	def loadData(self, input):
		
		raw = pd.read_csv(input, sep='\t', index_col='Time')
		raw.index = pd.to_datetime(raw.index, dayfirst=True)

		return raw



class quitDialog(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Message box')
		self.show()

	def closeEvent(self, event):

		reply = QMessageBox.question(self, 'Message',
									 "Are you sure to quit?", QMessageBox.Yes |
									 QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:

			event.accept()
		else:

			event.ignore()



# class TideWidget(QWidget):

# 	def __init__(self):
# 		super().__init__()

# 		self.initUI()


# 	def initUI(self):

# 		vbox = QVBoxLayout(self)

# 		plotSample = QFrame(self)
# 		plotSample.setFrameShape(QFrame.StyledPanel)

# 		plotPredict = QFrame(self)
# 		plotPredict.setFrameShape(QFrame.StyledPanel)

# 		loadFrame = QTextEdit(QFrame(self))
# 		loadFrame.setFrameShape(QFrame.StyledPanel)

# 		splitPlot = QSplitter(Qt.Vertical)
# 		splitPlot.addWidget(plotSample)
# 		splitPlot.addWidget(self.loadFrame)
# 		splitPlot.addWidget(plotPredict)

# 		splitLoad = QSplitter(Qt.Horizontal)
# 		splitLoad.addWidget(splitPlot)

# 		vbox.addWidget(loadFrame)
# 		# vbox.addWidget(splitLoad)
# 		self.setLayout(vbox)
	

# 	# def loadDialog(self):

# 	# 	home_dir = str(Path.home())
# 	# 	fname = QFileDialog.getOpenFileName(self, 'Load file', home_dir)

# 	# 	if fname[0]:
# 	# 		f = open(fname[0], 'r')

# 	# 		with f:
# 	# 			data = f.read()
				
# 	# 			self.loadFrame.setText(data)
	
	
# 	def plotLoad(self, data):
		
# 		plt.figure(figsize=(20, 10))
# 		plt.plot(at, ad, label='Data Pasang Surut Sampel')
# 		plt.xlabel('Waktu')
# 		plt.ylabel('Ketinggian Muka Air dari Sensor (m)')
# 		plt.legend(loc='best')
# 		plt.show()



def main():

	app = QApplication(sys.argv)
	tide = TideMain()
	tide.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
