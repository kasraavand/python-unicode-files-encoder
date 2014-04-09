import sys
import os
from PyQt4 import QtGui, QtCore
import codecs

class TestListView(QtGui.QDialog):
    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)
        #self.setIconSize(QtCore.QSize(72, 72))
        self.createFilesTable()
        findButton = self.createButton("&Decode", self.find)
        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(findButton)
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.filesTable, 3, 0, 1, 3)
        browseButton = self.createButton("&Browse...", self.browse)
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        directoryLabel = QtGui.QLabel("Your Path:")
        mainLayout.addWidget(directoryLabel, 2, 0)
        mainLayout.addWidget(self.directoryComboBox, 2, 1)
        mainLayout.addWidget(browseButton, 2, 2)
        mainLayout.addLayout(buttonsLayout, 5, 0, 1, 3)
        self.setLayout(mainLayout)
        #self.obj=MainForm(self)
        #self.connect(QtCore.SIGNAL("dropped"), self.find)
    def browse(self):
        
        fileName = QtGui.QFileDialog.getOpenFileName(self)
        if fileName:
            inFile = QtCore.QFile(fileName)
            if not inFile.open(QtCore.QFile.ReadOnly):
                QtGui.QMessageBox.warning(self, "Codecs",
                        "Cannot read file %s:\n%s" % (fileName, inFile.errorString()))
                return

            #data = inFile.readAll()
        
        self.showFiles(fileName)

    def showFiles(self, files):
      
            file = QtCore.QFile(files)
            size = QtCore.QFileInfo(file).size()

            fileNameItem = QtGui.QTableWidgetItem(files)
            fileNameItem.setFlags(fileNameItem.flags() ^ QtCore.Qt.ItemIsEditable)
            sizeItem = QtGui.QTableWidgetItem("%d KB" % (int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        return comboBox


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

    def createFilesTable(self):
        self.filesTable = QtGui.QTableWidget(0, 2)
        self.itemm=QtGui.QTableWidgetItem()
        self.filesTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(True)
        self.filesTable.cellActivated.connect(self.find)
        
    def find(self,fileName):
        
        row = self.filesTable.rowCount()
        #self.filesTable.setRowCount(0)
        #fileName = self.comboBox.currentText()
        #text = self.textComboBox.currentText()
        path = self.directoryComboBox.currentText()
        #self.updateComboBox(self.fileComboBox)
        #self.updateComboBox(self.textComboBox)
        self.updateComboBox(self.directoryComboBox)
        self.currentDir = QtCore.QDir(path)
        #self.showFiles(files)
        #file = QtCore.QFile(files)
        #fileNameItem = QtGui.QTableWidgetItem(files)
        #fileNameItem.setFlags(fileNameItem.flags() ^ QtCore.Qt.ItemIsEditable)
        
	
        #self.crName.setText(item.text())
        #print a.text()
        for i in range(row):
         item = self.filesTable.item(i,0)
         a=QtGui.QTableWidgetItem(item)
         file=codecs.open('%s'%a.text(), encoding='WINDOWS-1256')
         data = file.read()
         with open('%s'%a.text(),'w') as r :
          r.write(data.encode('utf8'))

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.view = TestListView(self)
        self.connect(self.view, QtCore.SIGNAL("dropped"), self.pictureDropped)
        self.setCentralWidget(self.view)
        self.resize(700, 300)

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)                
                icon = QtGui.QIcon(url)
                pixmap = icon.pixmap(72, 72)                
                icon = QtGui.QIcon(pixmap)
                self.view.showFiles(url)
                #item = QtGui.QListWidgetItem(url, self.view)
                #item.setIcon(icon)        
                #item.setStatusTip(url)       
        
def main():
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
