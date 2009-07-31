import sys
from PyQt4 import QtCore, QtGui

from ReplayUploader import ReplayUploader

import Config

W, H = 250, 75

class Uploader(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.uploader = ReplayUploader(Config.upload_url)
        self.setWindowFlags(QtCore.Qt.ToolTip)

        self.setMinimumSize(W, H)
        self.setMaximumSize(W, H)
        desktop = QtGui.QApplication.desktop()
        w, h = desktop.width(), desktop.height()
        self.move(w-W-10, h-H-10)

        self.createActions()
        self.createTrayIcon()
        self.createDisplay()
        self.trayIcon.show()

    def createDisplay(self):
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.move(10, 40)
        self.progressBar.setMinimumSize(W-20, 20)
        self.progressBar.setMaximumSize(W-20, 20)

        self.label = QtGui.QLabel(self)
        self.label.move(10, 10)
        self.label.setText("Label")

    def createActions(self):
        self.quitAction = QtGui.QAction(self.tr("&Quit"), self)
        QtCore.QObject.connect(
                self.quitAction, QtCore.SIGNAL("triggered()"),
                QtGui.qApp, QtCore.SLOT("quit()"))

        #self.uploadAction = QtGui.QAction(self.tr("&Upload"), self)

    def upload(self):
        self.show()

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon('trayicon.gif'))
        QtCore.QObject.connect(
                self.trayIcon, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
                self.upload)

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    frame = Uploader()
    sys.exit(app.exec_())
