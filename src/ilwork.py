import sys
import os
from typing import Dict
from PyQt5 import QtCore, QtWidgets

import ui.frm_main

import image_view

import widget_potrace
import widget_watershed
import widget_check
import widget_x_test


class CWidgetManager(object):
    # 開発したプログラムにUIをつけて動作させるためのクラス
    window: QtWidgets.QMainWindow = None
    items: Dict[QtWidgets.QAction, QtWidgets.QWidget] = None

    def __init__(self, _window: QtWidgets.QMainWindow):
        self.window = _window
        self.items = {}

    def set(self, action: QtWidgets.QAction):
        for item in self.items.keys():
            item.setChecked(False)

        dock = self.window.findChild(QtWidgets.QDockWidget)
        tool = dock.findChild(QtWidgets.QToolBox)

        while tool.count() > 0:
            widget = tool.widget(0)
            if hasattr(widget, "custom_term") is True:
                widget.custom_term()
            tool.removeItem(0)

        widget = self.items[action]
        if hasattr(widget, "custom_init") is True:
            widget.custom_init()
        tool.addItem(widget, widget.windowTitle())
        action.setChecked(True)


class CMainWindow(QtWidgets.QMainWindow):
    view: image_view.CView = None
    widgets: CWidgetManager = None

    def __init__(self):
        super(CMainWindow, self).__init__()

        self.ui = ui.frm_main.Ui_MainWindow()
        self.ui.setupUi(self)

        self.view = image_view.CView(self)
        self.setCentralWidget(self.view)

        self.ui.ac_file_new.setEnabled(False)
        self.ui.ac_file_open.triggered.connect(self.evt_file_open)
        self.ui.ac_file_export.triggered.connect(self.evt_file_export)

        # for CWidgetManager
        # ----
        self.ui.ac_potrace.triggered.connect(self.evt_potrace)
        self.ui.ac_watershed.triggered.connect(self.evt_watershed)
        self.ui.ac_check.triggered.connect(self.evt_check)
        self.ui.ac_widget_x_test.triggered.connect(self.evt_widget_x_test)

        self.widgets = CWidgetManager(self)
        self.widgets.items[self.ui.ac_potrace] = widget_potrace.CWidget(self.view)
        self.widgets.items[self.ui.ac_watershed] = widget_watershed.CWidget(self.view)
        self.widgets.items[self.ui.ac_check] = widget_check.CWidget(self.view)
        self.widgets.items[self.ui.ac_widget_x_test] = widget_x_test.CWidget(self.view)
        # ----

    def evt_file_open(self):

        o_dlg = QtWidgets.QFileDialog(self)
        o_dlg.setWindowModality(QtCore.Qt.WindowModal)
        o_dlg.setNameFilter("Image file (*.bmp *.png *.jpg *.jpeg *.webp)")
        o_dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        o_dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        o_dlg.setModal(True)

        def signal_finished(result):
            if result == QtWidgets.QDialog.Accepted:
                for pathname in o_dlg.selectedFiles():
                    self.view.open(pathname)
                    break

        o_dlg.finished.connect(signal_finished)
        o_dlg.show()

    def evt_file_export(self):

        o_dlg = QtWidgets.QFileDialog(self)
        o_dlg.setWindowModality(QtCore.Qt.WindowModal)
        if self.ui.ac_potrace.isChecked() is True:
            o_dlg.setNameFilter("SVG file (*.svg)")
        else:
            o_dlg.setNameFilter("Image file (*.bmp *.eps *.png *.jpg *.jpeg *.webp)")
        o_dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        o_dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        o_dlg.setModal(True)

        def signal_finished(result):
            if result == QtWidgets.QDialog.Accepted:
                for pathname in o_dlg.selectedFiles():
                    result = self.view.export(pathname)
                    if result is False:
                        dlg_err = QtWidgets.QErrorMessage()
                        dlg_err.showMessage("Failure")
                    break

        o_dlg.finished.connect(signal_finished)
        o_dlg.show()

    def evt_potrace(self):
        self.widgets.set(self.ui.ac_potrace)

    def evt_watershed(self):
        self.widgets.set(self.ui.ac_watershed)

    def evt_check(self):
        self.widgets.set(self.ui.ac_check)

    def evt_widget_x_test(self):
        self.widgets.set(self.ui.ac_widget_x_test)


def main():
    instance = QtWidgets.QApplication(sys.argv)

    if instance is not None:

        for locale_text in QtCore.QLocale().uiLanguages():
            translator = QtCore.QTranslator()

            dir_name, _ = os.path.split(sys.argv[0])
            dir_name = os.path.join(dir_name, "lang")
            qm_pathname = os.path.join(dir_name, "ilwork_{:s}.qm".format(locale_text))
            res = translator.load(qm_pathname)
            if res is True:
                instance.installTranslator(translator)
                break

        o_main = CMainWindow()
        o_main.show()

        instance.exec()

    return 0


if __name__ == "__main__":
    sys.exit(main())
