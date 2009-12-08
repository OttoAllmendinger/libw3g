import os
import os.path as P
import sys
import time
import traceback
import subprocess

from PyQt4 import QtCore, QtGui

import ReplayUploader
import Config


W, H = 300, 400

class Uploader:
    def __init__(self, app):
        self.app = app
        self.w = self.create_main_window()

        self.dotastats_host = self.get_var('host', 
                self.input_host, self.verify_host)
        self.uploader = ReplayUploader.ReplayUploader(
                'http://%s' % self.dotastats_host)

        self.tft_exe_path = self.get_var('tft_exe_path', 
                self.input_tft_exe, self.verify_tft_exe)

        self.w.show()

        self.log('ReplayUploader started...')
        self.log('host: %s' % self.dotastats_host)
        #self.log('<a href="http://%s/">site</a>' % dotastats_host)
        self.log('tft_exe_path: %s' % self.tft_exe_path)

        if Config.get('tft_autostart', False):
            self.start_tft()

        self.check_replay_timer = QtCore.QTimer()
        QtCore.QObject.connect(
                self.check_replay_timer, QtCore.SIGNAL("timeout()"),
                self.check_replay)
        self.check_replay_timer.start(1000)

    def get_last_replay_path(self):
        return P.join(P.dirname(self.tft_exe_path), 'replay', 'LastReplay.w3g')

    def get_var(self, name, cb_input=None, cb_verify=None):
        config = Config.load()
        value = Config.get(name)

        try:
            cb_verify(value)
        except:
            value = cb_input()
            cb_verify(value)

        Config.set(name, value)
        return value


    def verify_host(self, host):
        return ReplayUploader.test_host(unicode(host))

    def input_host(self): 
        host, ok = QtGui.QInputDialog.getText(self.w, 
                self.w.tr("Please Enter Hostname"),
                self.w.tr("Hostname:"), QtGui.QLineEdit.Normal)

        return unicode(host) if ok else None

    def verify_tft_exe(self, tft_exe):
        assert os.path.exists(tft_exe)

    def input_tft_exe(self):
        path = QtGui.QFileDialog.getOpenFileName(self.w,
                self.w.tr("Select Frozen Throne Program"), "/", 
                "TFT Executable (*.exe)")

        return unicode(path)

    def create_main_window(self):
        config = Config.load()

        w = QtGui.QWidget()
        w.setWindowTitle('Dota Replay Uploader 0.1')
        w.setWindowFlags(QtCore.Qt.Dialog)
        w.setMinimumSize(W, H)
        w.setMaximumSize(W, H)

        l = QtGui.QVBoxLayout()

        self.status_box = sb = QtGui.QListWidget(w)
        sb.setWrapping(True)
        l.addWidget(sb, 1)

        b = QtGui.QPushButton("&Start TFT...", w)
        QtCore.QObject.connect(
                b, QtCore.SIGNAL('clicked()'), self.start_tft)
        l.addWidget(b)

        self.cb_autostart = cb = QtGui.QCheckBox(
                w.tr("Start &automatically"), w)
        cb.setChecked(Config.get('tft_autostart', False))
        QtCore.QObject.connect(
                cb, QtCore.SIGNAL('clicked()'), self.trigger_autostart)
        l.addWidget(cb)

        w.setLayout(l)

        return w

    def trigger_autostart(self):
        Config.set('tft_autostart', self.cb_autostart.isChecked())

    def start_tft(self):
        self.log("starting tft...")
        subprocess.Popen(self.tft_exe_path)

    def upload_last_replay(self):
        replay_path = self.get_last_replay_path()
        self.log('uploading replay...')
        if self.uploader.exists(replay_path):
            self.log('replay already exists')
        else:
            self.uploader.upload(replay_path)
            self.log('done uploading replay')

    def check_replay(self):
        replay_ts = ReplayUploader.get_timestamp(
                self.get_last_replay_path())
        if not hasattr(self, 'last_replay_ts'):
            self.last_replay_ts = 0
        elif replay_ts != self.last_replay_ts:
            self.last_replay_ts = replay_ts
            self.upload_last_replay()

    def log(self, eventStr):
        self.status_box.addItem("%s - %s" % (
            time.strftime("%H:%M:%S", time.localtime(time.time())),
            eventStr))
    

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    frame = Uploader(app)
    sys.exit(app.exec_())
