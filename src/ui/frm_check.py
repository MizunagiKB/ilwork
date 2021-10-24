# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/frm_check.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 414)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.slider_transparent = QtWidgets.QSlider(Form)
        self.slider_transparent.setMinimum(25)
        self.slider_transparent.setMaximum(100)
        self.slider_transparent.setSingleStep(25)
        self.slider_transparent.setPageStep(25)
        self.slider_transparent.setProperty("value", 50)
        self.slider_transparent.setOrientation(QtCore.Qt.Horizontal)
        self.slider_transparent.setObjectName("slider_transparent")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.slider_transparent)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.push_saliency = QtWidgets.QPushButton(self.groupBox_2)
        self.push_saliency.setObjectName("push_saliency")
        self.verticalLayout_3.addWidget(self.push_saliency)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spinbox_colors = QtWidgets.QSpinBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_colors.sizePolicy().hasHeightForWidth())
        self.spinbox_colors.setSizePolicy(sizePolicy)
        self.spinbox_colors.setMinimumSize(QtCore.QSize(64, 0))
        self.spinbox_colors.setPrefix("")
        self.spinbox_colors.setMinimum(1)
        self.spinbox_colors.setMaximum(16)
        self.spinbox_colors.setProperty("value", 8)
        self.spinbox_colors.setObjectName("spinbox_colors")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinbox_colors)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinbox_number_of_times = QtWidgets.QSpinBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_number_of_times.sizePolicy().hasHeightForWidth())
        self.spinbox_number_of_times.setSizePolicy(sizePolicy)
        self.spinbox_number_of_times.setMinimumSize(QtCore.QSize(64, 0))
        self.spinbox_number_of_times.setMinimum(1)
        self.spinbox_number_of_times.setMaximum(16)
        self.spinbox_number_of_times.setProperty("value", 6)
        self.spinbox_number_of_times.setObjectName("spinbox_number_of_times")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinbox_number_of_times)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.push_kmeans = QtWidgets.QPushButton(self.groupBox)
        self.push_kmeans.setObjectName("push_kmeans")
        self.verticalLayout_2.addWidget(self.push_kmeans)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.push_gradcam = QtWidgets.QPushButton(self.groupBox_3)
        self.push_gradcam.setObjectName("push_gradcam")
        self.verticalLayout_4.addWidget(self.push_gradcam)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "check"))
        self.label_3.setText(_translate("Form", "Transparent"))
        self.groupBox_2.setTitle(_translate("Form", "OpenCV"))
        self.push_saliency.setText(_translate("Form", "Saliency"))
        self.groupBox.setTitle(_translate("Form", "PIL.ImageFilter - quantize"))
        self.label.setText(_translate("Form", "Colors"))
        self.label_2.setText(_translate("Form", "Number of Times"))
        self.push_kmeans.setText(_translate("Form", "Update kmeans"))
        self.groupBox_3.setTitle(_translate("Form", "nnabla"))
        self.push_gradcam.setText(_translate("Form", "GradCAM"))