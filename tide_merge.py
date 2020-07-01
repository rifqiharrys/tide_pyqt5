#!/usr/bin/python3

import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QLineEdit, QFileDialog, QDialog,
                             QGridLayout, QMessageBox, QVBoxLayout, QComboBox, QLabel, QPushButton,
                             QTableWidgetItem, QSpinBox, QScrollArea, QCheckBox, QTextBrowser)
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

        loadFilesButton = QPushButton('Load Data')
        loadFilesButton.clicked.connect(self.loadDataDialog)

        sepOutLabel = QLabel('Output Separator:')
        self.sepOutCB = QComboBox()
        self.sepOutCB.addItems(['Tab', 'Comma', 'Semicolon'])

        saveLocButton = QPushButton('Save File Location')
        saveLocButton.clicked.connect(self.savePathDialog)
        self.saveLocLineForm = QLineEdit()

        startButton =  QPushButton('Start Merge')
        startButton.clicked.connect(self.startMerge)
        startButton.clicked.connect(self.close)

        self.table = QTableWidget()
        scroll = QScrollArea()
        scroll.setWidget(self.table)

        self.dataFrame = QTextBrowser()

        closeButton = QPushButton('Close')
        closeButton.clicked.connect(self.close)

        grid = QGridLayout()
        vbox = QVBoxLayout()

        grid.addWidget(loadFilesButton, 1, 1, 1, 2)
        grid.addWidget(sepOutLabel, 1, 3, 1, 1)
        grid.addWidget(self.sepOutCB, 1, 4, 1, 1)

        grid.addWidget(saveLocButton, 2, 1, 1, 1)
        grid.addWidget(self.saveLocLineForm, 2, 2, 1, 2)
        grid.addWidget(startButton, 2, 4, 1, 1)

        grid.addWidget(self.table, 3, 1, 97, 4)

        vbox.addStretch(1)
        grid.addLayout(vbox, 101, 1)
        grid.addWidget(closeButton, 102, 4, 1, 1)
        self.setLayout(grid)

    def loadDataDialog(self):

        loadData = QDialog()
        loadData.setWindowTitle('Load Data')
        loadData.setWindowIcon(QIcon('load-pngrepo-com.png'))

        openFilesButton = QPushButton('Open File(s)')
        openFilesButton.clicked.connect(self.filesDialog)
        openFolderButton = QPushButton('Open Folder')
        openFolderButton.clicked.connect(self.folderDialog)

        sepInLabel = QLabel('Separator:')
        self.sepInCB = QComboBox()
        self.sepInCB.addItems(['Tab', 'Comma', 'Space', 'Semicolon'])

        textTypeLabel = QLabel('Text Type')
        self.textTypeCB = QComboBox()
        self.textTypeCB.addItems(['.txt', '.csv', '.dat'])

        headerLineLabel = QLabel('Header Starting Line:')
        self.headerLineSB = QSpinBox()
        self.headerLineSB.setMinimum(1)

        dataLineLabel = QLabel('Data Starting Line:')
        self.dataLineSB = QSpinBox()
        self.dataLineSB.setMinimum(1)

        locLabel = QLabel('Location:')
        self.locList = QTextBrowser()

        self.showCheckBox = QCheckBox('Show All Data to Table')
        self.showCheckBox.setChecked(False)
        self.showCheckBox.toggled.connect(self.showCheckBoxState)
        self.showState = QLabel()

        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(loadData.close)
        loadButton = QPushButton('Load')
        loadButton.clicked.connect(self.loadAction)
        loadButton.clicked.connect(loadData.close)

        grid = QGridLayout()
        grid.addWidget(openFilesButton, 1, 1, 1, 2)
        grid.addWidget(openFolderButton, 1, 3, 1, 2)

        grid.addWidget(sepInLabel, 2, 1, 1, 1)
        grid.addWidget(self.sepInCB, 2, 2, 1, 1)
        grid.addWidget(textTypeLabel, 2, 3, 1, 1)
        grid.addWidget(self.textTypeCB, 2, 4, 1, 1)

        grid.addWidget(headerLineLabel, 3, 1, 1, 1)
        grid.addWidget(self.headerLineSB, 3, 2, 1, 1)
        grid.addWidget(dataLineLabel, 3, 3, 1, 1)
        grid.addWidget(self.dataLineSB, 3, 4, 1, 1)

        grid.addWidget(locLabel, 4, 1, 1, 1)

        grid.addWidget(self.locList, 5, 1, 10, 4)

        grid.addWidget(self.showCheckBox, 15, 1, 1, 2)
        grid.addWidget(loadButton, 15, 3, 1, 1)
        grid.addWidget(cancelButton, 15, 4, 1, 1)

        loadData.setLayout(grid)

        loadData.exec_()

    def showCheckBoxState(self):

        if self.showCheckBox.isChecked() == True:
            self.showState.setText(self.showCheckBox.text())
        else:
            self.showState.setText('unchecked')

    def filesDialog(self):

        home_dir = str(Path.home())
        fileFilter = 'Text Files (*.txt *.csv *.dat)'
        fname = QFileDialog.getOpenFileNames(self, 'Open File(s)', home_dir, fileFilter)

        global filesList
        filesList = fname[0]

        fileListPrint = ''

        for file in filesList:
            fileListPrint += file + '\n'

        self.locList.setText(fileListPrint)

    def folderDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getExistingDirectory(self, 'Open Folder', home_dir)

        textTypeDict = {'.txt': '.[Tt][Xx][Tt]', '.csv': '.[Cc][Ss][Vv]', '.dat': '.[Dd][Aa][Tt]'}
        textTypeSelect = textTypeDict[self.textTypeCB.currentText()]

        pathName = fname + '/**/*' + textTypeSelect

        global filesList
        filesList = glob.glob(pathName, recursive=True)

        fileListPrint = ''

        for file in filesList:
            fileListPrint += file + '\n'

        self.locList.setText(fileListPrint)

    def loadDataDict(self):

        head = self.headerLineSB.value() - 1
        start_data = self.dataLineSB.value() - 1
        sepInDict = {'Tab': '\t', 'Comma': ',', 'Space': ' ', 'Semicolon': ';'}
        sepInSelect = sepInDict[self.sepInCB.currentText()]

        dummy = []

        for file in filesList:
            raw = pd.read_csv(file, sep=sepInSelect, header=head)
            raw = raw.iloc[start_data:, 0:]

            dummy.append(raw)

        global merged
        merged = pd.concat(dummy, ignore_index=True, sort=False)

        return merged

    def loadAction(self):

        raw = self.loadDataDict()

        if self.showState.text() == 'Show All Data to Table':
            data = raw
        else:
            data = raw.head(100)

        self.table.setColumnCount(len(data.columns))
        self.table.setRowCount(len(data.index))

        for h in range(len(data.columns)):
            self.table.setHorizontalHeaderItem(h, QTableWidgetItem(data.columns[h]))

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(data.iloc[i, j])))

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()


    def savePathDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getSaveFileName(self, 'Save File', home_dir, 'Text files (*.txt)')
        filePath = (str(Path(fname[0])))
        self.saveLocLineForm.setText(filePath)


    def startMerge(self):

        save_file = self.saveLocLineForm.text()
        sepOutDict = {'Tab': '\t', 'Comma': ',', 'Semicolon': ';'}
        sepOutSelect = sepOutDict[self.sepOutCB.currentText()]
        data = merged

        data.to_csv(save_file, sep=sepOutSelect, index=False)



def main():

    global merge
    merge = MergeData()
    merge.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())
