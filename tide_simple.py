# #!/usr/bin/python3

# import sys
# from pathlib import Path
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QInputDialog, QAction, QHBoxLayout, QVBoxLayout, QFrame, QSplitter, QPushButton)
# from PyQt5.QtGui import QIcon
# from tdr_py.vp_tide import v_merge, v_dirmerge
# from ttide import t_tide, t_utils
# from utide import solve, reconstruct
# import pandas as pd
# import numpy as np
# from matplotlib.dates import date2num
# import matplotlib.pyplot as plt
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()


# class TideSimple(QWidget):

# 	def __init__(self):
# 		super().__init__()

# 		self.initUI()


# 	def initUI(self):

# 		self.setGeometry(300, 300, 480, 640)
# 		self.setWindowTitle('Tide')
# 		self.setWindowIcon(QIcon('wave-pngrepo-com.png'))

# 		ttideButton = QPushButton('T Tide Tidal Analysis')
# 		ttideButton.clicked.connect(self.ttide)

# 		vbox = QVBoxLayout(self)

# 		vbox.addWidget(ttideButton)


# 		vbox.addStretch(1)
# 		self.setLayout(vbox)

# 		# loaded = self.loadDialog

# 		# plotSample = QFrame(self)
# 		# plotSample.setFrameShape(QFrame.StyledPanel)

# 		# plotPredict = QFrame(self)
# 		# plotPredict.setFrameShape(QFrame.StyledPanel)

# 	def ttide(self):

# 		home_dir = str(Path.home())
# 		fname = QFileDialog.getOpenFileName(self, 'Load file', home_dir)
# 		filePath = str(Path(fname[0]))
# 		raw = pd.read_csv(filePath, sep='\t', index_col='Timestamp')
# 		raw.index = pd.to_datetime(raw.index, dayfirst=True)
		
# 		ad = raw['Depth'].values
# 		demeaned_ad = ad - np.nanmean(ad)
		
# 		at = raw.index
# 		time = date2num(at.to_pydatetime())

# 		tfit_d = t_tide(ad, dt=1/12, stime=time[0], lat=5.275273, synth=0)



# 		# if fname[0]:
# 		# 	f = open(fname[0], 'r')
# 		# 	# raw = self.convertLoad(f)

# 		# 	with f:
# 		# 		data = f.read()
# 		# 		self.locationFrame.setText(data)

# 		# raw = pd.read_csv(data, sep='\t', index_col='Time')
# 		# raw.index = pd.to_datetime(raw.index, dayfirst=True)

# 		# return raw


# def main():

# 	app = QApplication(sys.argv)
# 	tide = TideSimple()
# 	tide.show()
# 	sys.exit(app.exec_())


# if __name__ == '__main__':
# 	main()

import sys
from PyQt5 import QtWidgets


class LoginDlg(QtWidgets.QDialog):

	def __init__(self):
		super(LoginDlg, self).__init__()

		self.password = QtWidgets.QLineEdit()
		self.password.setEchoMode(QtWidgets.QLineEdit.Password)
		self.button_box = QtWidgets.QDialogButtonBox(
			QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)

		layout = QtWidgets.QFormLayout()
		layout.setFieldGrowthPolicy(
			QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
		layout.addRow('Password', self.password)
		layout.addWidget(self.button_box)

		self.setLayout(layout)
		self.setWindowTitle("Login")
		self.setMinimumWidth(350)


class MyWindow(QtWidgets.QWidget):

	def __init__(self):
		super(MyWindow, self).__init__()

		self.edit = QtWidgets.QLineEdit()
		button = QtWidgets.QPushButton("Get input from dialog")
		button.clicked.connect(self.get_login)
		layout = QtWidgets.QHBoxLayout()
		layout.addWidget(self.edit)
		layout.addWidget(button)
		self.setLayout(layout)

	def get_login(self):
		login = LoginDlg()
		if login.exec_():
			self.edit.setText(login.password.text())


if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	window = MyWindow()
	window.show()
	sys.exit(app.exec_())
