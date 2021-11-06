# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/frm_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setMinimumSize(QtCore.QSize(224, 165))
        self.dockWidget.setFloating(False)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtWidgets.QToolBox(self.dockWidgetContents)
        self.toolBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setBaseSize(QtCore.QSize(0, 0))
        self.toolBox.setObjectName("toolBox")
        self.init = QtWidgets.QWidget()
        self.init.setGeometry(QtCore.QRect(0, 0, 218, 415))
        self.init.setObjectName("init")
        self.toolBox.addItem(self.init, "")
        self.verticalLayout.addWidget(self.toolBox)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.toolBar1 = QtWidgets.QToolBar(MainWindow)
        self.toolBar1.setIconSize(QtCore.QSize(24, 24))
        self.toolBar1.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar1.setObjectName("toolBar1")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar1)
        self.toolBar2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar2.setIconSize(QtCore.QSize(24, 24))
        self.toolBar2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar2.setObjectName("toolBar2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar2)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.ac_potrace = QtWidgets.QAction(MainWindow)
        self.ac_potrace.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/pen-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_potrace.setIcon(icon)
        self.ac_potrace.setObjectName("ac_potrace")
        self.ac_watershed = QtWidgets.QAction(MainWindow)
        self.ac_watershed.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/fill-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_watershed.setIcon(icon1)
        self.ac_watershed.setObjectName("ac_watershed")
        self.ac_check = QtWidgets.QAction(MainWindow)
        self.ac_check.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/vial-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_check.setIcon(icon2)
        self.ac_check.setObjectName("ac_check")
        self.ac_file_open = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/folder-open-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_file_open.setIcon(icon3)
        self.ac_file_open.setObjectName("ac_file_open")
        self.ac_file_export = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/file-export-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_file_export.setIcon(icon4)
        self.ac_file_export.setObjectName("ac_file_export")
        self.ac_file_new = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/res/file-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_file_new.setIcon(icon5)
        self.ac_file_new.setStatusTip("")
        self.ac_file_new.setObjectName("ac_file_new")
        self.ac_view_zoom_in = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/res/search-plus-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_view_zoom_in.setIcon(icon6)
        self.ac_view_zoom_in.setObjectName("ac_view_zoom_in")
        self.ac_view_zoom_out = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/res/search-minus-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_view_zoom_out.setIcon(icon7)
        self.ac_view_zoom_out.setObjectName("ac_view_zoom_out")
        self.ac_zoom_reset = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/res/search-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_zoom_reset.setIcon(icon8)
        self.ac_zoom_reset.setObjectName("ac_zoom_reset")
        self.ac_image_src = QtWidgets.QAction(MainWindow)
        self.ac_image_src.setCheckable(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/res/image-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_image_src.setIcon(icon9)
        self.ac_image_src.setObjectName("ac_image_src")
        self.ac_image_dst = QtWidgets.QAction(MainWindow)
        self.ac_image_dst.setCheckable(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/res/image-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_image_dst.setIcon(icon10)
        self.ac_image_dst.setObjectName("ac_image_dst")
        self.ac_scroll_hand_drag = QtWidgets.QAction(MainWindow)
        self.ac_scroll_hand_drag.setObjectName("ac_scroll_hand_drag")
        self.ac_widget_x_test = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/res/cubes-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_widget_x_test.setIcon(icon11)
        self.ac_widget_x_test.setObjectName("ac_widget_x_test")
        self.toolBar1.addAction(self.ac_file_new)
        self.toolBar1.addAction(self.ac_file_open)
        self.toolBar1.addAction(self.ac_file_export)
        self.toolBar2.addAction(self.ac_potrace)
        self.toolBar2.addAction(self.ac_watershed)
        self.toolBar2.addAction(self.ac_check)
        self.toolBar2.addSeparator()
        self.toolBar2.addAction(self.ac_widget_x_test)
        self.toolBar.addAction(self.ac_image_src)
        self.toolBar.addAction(self.ac_image_dst)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.ac_zoom_reset)
        self.toolBar.addAction(self.ac_view_zoom_out)
        self.toolBar.addAction(self.ac_view_zoom_in)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ilWork"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "tool"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.init), _translate("MainWindow", "Blank"))
        self.toolBar1.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.toolBar2.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.ac_potrace.setText(_translate("MainWindow", "Potrace"))
        self.ac_potrace.setToolTip(_translate("MainWindow", "Potrace"))
        self.ac_watershed.setText(_translate("MainWindow", "Watershed"))
        self.ac_watershed.setToolTip(_translate("MainWindow", "Watershed"))
        self.ac_check.setText(_translate("MainWindow", "Check"))
        self.ac_check.setToolTip(_translate("MainWindow", "Check"))
        self.ac_file_open.setText(_translate("MainWindow", "FileOpen"))
        self.ac_file_open.setToolTip(_translate("MainWindow", "FileOpen"))
        self.ac_file_open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.ac_file_export.setText(_translate("MainWindow", "FileExport"))
        self.ac_file_export.setToolTip(_translate("MainWindow", "FileExport"))
        self.ac_file_new.setText(_translate("MainWindow", "FileNew"))
        self.ac_file_new.setToolTip(_translate("MainWindow", "FileNew"))
        self.ac_view_zoom_in.setText(_translate("MainWindow", "ZoomIn"))
        self.ac_view_zoom_in.setToolTip(_translate("MainWindow", "ZoomIn"))
        self.ac_view_zoom_in.setStatusTip(_translate("MainWindow", "ZoomIn"))
        self.ac_view_zoom_out.setText(_translate("MainWindow", "ZoomOut"))
        self.ac_view_zoom_out.setToolTip(_translate("MainWindow", "ZoomOut"))
        self.ac_view_zoom_out.setStatusTip(_translate("MainWindow", "ZoomOut"))
        self.ac_zoom_reset.setText(_translate("MainWindow", "ZoomReset"))
        self.ac_zoom_reset.setToolTip(_translate("MainWindow", "ZoomReset"))
        self.ac_image_src.setText(_translate("MainWindow", "ImageSrc"))
        self.ac_image_src.setToolTip(_translate("MainWindow", "ImageSrc"))
        self.ac_image_dst.setText(_translate("MainWindow", "ImageDst"))
        self.ac_image_dst.setToolTip(_translate("MainWindow", "ImageDst"))
        self.ac_scroll_hand_drag.setText(_translate("MainWindow", "ScrollHandDrag"))
        self.ac_scroll_hand_drag.setToolTip(_translate("MainWindow", "ScrollHandDrag"))
        self.ac_scroll_hand_drag.setShortcut(_translate("MainWindow", "Space"))
        self.ac_widget_x_test.setText(_translate("MainWindow", "Test"))
        self.ac_widget_x_test.setToolTip(_translate("MainWindow", "Test"))
import resource
