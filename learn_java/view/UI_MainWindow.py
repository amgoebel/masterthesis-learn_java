# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1101, 688)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hL_mainFields = QtWidgets.QHBoxLayout()
        self.hL_mainFields.setObjectName("hL_mainFields")
        self.vL_Information = QtWidgets.QVBoxLayout()
        self.vL_Information.setObjectName("vL_Information")
        self.l_Lehrgang = QtWidgets.QLabel(parent=self.centralwidget)
        self.l_Lehrgang.setObjectName("l_Lehrgang")
        self.vL_Information.addWidget(self.l_Lehrgang)
        self.tB_information = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.tB_information.setObjectName("tB_information")
        self.vL_Information.addWidget(self.tB_information)
        self.hL_mainFields.addLayout(self.vL_Information)
        self.vL_code = QtWidgets.QVBoxLayout()
        self.vL_code.setObjectName("vL_code")
        self.l_Code = QtWidgets.QLabel(parent=self.centralwidget)
        self.l_Code.setObjectName("l_Code")
        self.vL_code.addWidget(self.l_Code)
        self.pTE_code = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.pTE_code.setObjectName("pTE_code")
        self.vL_code.addWidget(self.pTE_code)
        self.hL_mainFields.addLayout(self.vL_code)
        self.vL_output_input = QtWidgets.QVBoxLayout()
        self.vL_output_input.setObjectName("vL_output_input")
        self.l_Output = QtWidgets.QLabel(parent=self.centralwidget)
        self.l_Output.setObjectName("l_Output")
        self.vL_output_input.addWidget(self.l_Output)
        self.lV_output = QtWidgets.QListView(parent=self.centralwidget)
        self.lV_output.setWordWrap(True)
        self.lV_output.setObjectName("lV_output")
        self.vL_output_input.addWidget(self.lV_output)
        self.l_Input = QtWidgets.QLabel(parent=self.centralwidget)
        self.l_Input.setObjectName("l_Input")
        self.vL_output_input.addWidget(self.l_Input)
        self.lE_input = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lE_input.setObjectName("lE_input")
        self.vL_output_input.addWidget(self.lE_input)
        self.pB_send = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_send.sizePolicy().hasHeightForWidth())
        self.pB_send.setSizePolicy(sizePolicy)
        self.pB_send.setObjectName("pB_send")
        self.vL_output_input.addWidget(self.pB_send)
        self.hL_mainFields.addLayout(self.vL_output_input)
        self.hL_mainFields.setStretch(0, 1)
        self.hL_mainFields.setStretch(1, 2)
        self.hL_mainFields.setStretch(2, 1)
        self.verticalLayout.addLayout(self.hL_mainFields)
        self.hL_buttons = QtWidgets.QHBoxLayout()
        self.hL_buttons.setContentsMargins(0, 0, -1, -1)
        self.hL_buttons.setObjectName("hL_buttons")
        self.pB_compile = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_compile.sizePolicy().hasHeightForWidth())
        self.pB_compile.setSizePolicy(sizePolicy)
        self.pB_compile.setObjectName("pB_compile")
        self.hL_buttons.addWidget(self.pB_compile)
        self.pB_run = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pB_run.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_run.sizePolicy().hasHeightForWidth())
        self.pB_run.setSizePolicy(sizePolicy)
        self.pB_run.setCheckable(True)
        self.pB_run.setObjectName("pB_run")
        self.hL_buttons.addWidget(self.pB_run)
        self.verticalLayout.addLayout(self.hL_buttons)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1101, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.l_Lehrgang.setText(_translate("MainWindow", "Lehrgang:"))
        self.l_Code.setText(_translate("MainWindow", "Dein Code:"))
        self.l_Output.setText(_translate("MainWindow", "Output / Information:"))
        self.l_Input.setText(_translate("MainWindow", "Input:"))
        self.pB_send.setText(_translate("MainWindow", "absenden"))
        self.pB_compile.setText(_translate("MainWindow", "kompilieren"))
        self.pB_run.setText(_translate("MainWindow", "start"))
