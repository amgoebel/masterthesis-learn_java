# Form implementation generated from reading ui file 'view/dialog_welcome.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_UI_Dialog_Welcome(object):
    def setupUi(self, UI_Dialog_Welcome):
        UI_Dialog_Welcome.setObjectName("UI_Dialog_Welcome")
        UI_Dialog_Welcome.resize(874, 597)
        UI_Dialog_Welcome.setMaximumSize(QtCore.QSize(1200, 600))
        self.verticalLayout = QtWidgets.QVBoxLayout(UI_Dialog_Welcome)
        self.verticalLayout.setObjectName("verticalLayout")
        self.l_text = QtWidgets.QLabel(parent=UI_Dialog_Welcome)
        self.l_text.setStyleSheet("font-size:16pt; color: rgb(0, 0, 255);")
        self.l_text.setObjectName("l_text")
        self.verticalLayout.addWidget(self.l_text)
        self.l_image = QtWidgets.QLabel(parent=UI_Dialog_Welcome)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_image.sizePolicy().hasHeightForWidth())
        self.l_image.setSizePolicy(sizePolicy)
        self.l_image.setMinimumSize(QtCore.QSize(144, 85))
        self.l_image.setMaximumSize(QtCore.QSize(1435, 850))
        self.l_image.setText("")
        self.l_image.setPixmap(QtGui.QPixmap("view/Screenshot_0.png"))
        self.l_image.setScaledContents(True)
        self.l_image.setObjectName("l_image")
        self.verticalLayout.addWidget(self.l_image)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pB_next_page = QtWidgets.QPushButton(parent=UI_Dialog_Welcome)
        self.pB_next_page.setLocale(QtCore.QLocale(QtCore.QLocale.Language.German, QtCore.QLocale.Country.Germany))
        self.pB_next_page.setObjectName("pB_next_page")
        self.horizontalLayout.addWidget(self.pB_next_page)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(UI_Dialog_Welcome)
        QtCore.QMetaObject.connectSlotsByName(UI_Dialog_Welcome)

    def retranslateUi(self, UI_Dialog_Welcome):
        _translate = QtCore.QCoreApplication.translate
        UI_Dialog_Welcome.setWindowTitle(_translate("UI_Dialog_Welcome", "Willkommen zu learn Java"))
        self.l_text.setText(_translate("UI_Dialog_Welcome", "Herzlich Willkommen"))
        self.pB_next_page.setText(_translate("UI_Dialog_Welcome", "Nächste Seite"))
