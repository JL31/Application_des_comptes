# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '01_Options_d_enregistrement.ui'
#
# Created: Mon Jan 21 17:01:57 2019
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(450, 150)
        Dialog.setMinimumSize(QtCore.QSize(450, 150))
        Dialog.setMaximumSize(QtCore.QSize(450, 150))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 95, 95))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 95, 95))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 95, 95))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(95, 95, 95))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Dialog.setPalette(palette)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(15, 15, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.CB_Enregistrement_copies = QtGui.QCheckBox(Dialog)
        self.CB_Enregistrement_copies.setMinimumSize(QtCore.QSize(400, 20))
        self.CB_Enregistrement_copies.setMaximumSize(QtCore.QSize(400, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_Enregistrement_copies.setFont(font)
        self.CB_Enregistrement_copies.setChecked(False)
        self.CB_Enregistrement_copies.setObjectName(_fromUtf8("CB_Enregistrement_copies"))
        self.horizontalLayout.addWidget(self.CB_Enregistrement_copies)
        spacerItem1 = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(15, 15, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.CB_Envoi_copies_fichiers_par_mail = QtGui.QCheckBox(Dialog)
        self.CB_Envoi_copies_fichiers_par_mail.setMinimumSize(QtCore.QSize(400, 20))
        self.CB_Envoi_copies_fichiers_par_mail.setMaximumSize(QtCore.QSize(400, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CB_Envoi_copies_fichiers_par_mail.setFont(font)
        self.CB_Envoi_copies_fichiers_par_mail.setChecked(False)
        self.CB_Envoi_copies_fichiers_par_mail.setObjectName(_fromUtf8("CB_Envoi_copies_fichiers_par_mail"))
        self.horizontalLayout_2.addWidget(self.CB_Envoi_copies_fichiers_par_mail)
        spacerItem3 = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(400, 20))
        self.label.setMaximumSize(QtCore.QSize(400, 20))
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem4 = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.B_Valider_options = QtGui.QPushButton(Dialog)
        self.B_Valider_options.setMinimumSize(QtCore.QSize(400, 40))
        self.B_Valider_options.setMaximumSize(QtCore.QSize(400, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.B_Valider_options.setFont(font)
        self.B_Valider_options.setAutoFillBackground(False)
        self.B_Valider_options.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0.5 rgba(70, 70, 70, 255), stop:1 rgba(200, 200, 200, 255));\n"
"color: rgb(240, 240, 240);"))
        self.B_Valider_options.setObjectName(_fromUtf8("B_Valider_options"))
        self.horizontalLayout_3.addWidget(self.B_Valider_options)
        spacerItem5 = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Options d\'enregistrement", None))
        self.CB_Enregistrement_copies.setText(_translate("Dialog", "Enregistrement d\'une copie des fichiers de données", None))
        self.CB_Envoi_copies_fichiers_par_mail.setText(_translate("Dialog", "Envoi d\'une copie des fichiers de données par mail", None))
        self.B_Valider_options.setText(_translate("Dialog", "Valider les options d\'enregistrement", None))

