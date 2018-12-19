import sys
import visa
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor


class PowerSupplyCommands:
    OUTPUT_ON = 'OUTP1 ON'
    OUTPUT_OFF = 'OUTP1 OFF'
    SET_VOLTAGE_1 = 'VOLT1 4'
    SET_VOLTAGE_2 = 'VOLT2 5'
    COUPLE_ALL = 'INST:COUP:OUTP:STAT ALL'
    DISPLAY_CH1 = 'DISP:CHAN 1'
    DISPLAY_CH2 = 'DISP:CHAN 2'
    ADDRESS = 'GPIB0::3::INSTR'
    GET_CURRENT_CH1 = 'MEAS:CURR1?'
    GET_CURRENT_CH2 = 'MEAS:CURR2?'


class UiDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.connected = False
        # self.ps = None
        self.event = None
        # self.rm = visa.ResourceManager()
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_ps_current)
        self.timer.start(500)

        QDialog.setObjectName(self, "Dialog")
        QDialog.resize(self, 400, 315)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 50, 181, 51))
        self.textEdit.setObjectName("textEdit")

        self.textEdit_2 = QtWidgets.QTextEdit(self)
        self.textEdit_2.setGeometry(QtCore.QRect(210, 50, 181, 51))
        self.textEdit_2.setObjectName("textEdit_2")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(10, 160, 181, 111))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.power_supply_commands(port_cmd=False, output_on=True))

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 160, 181, 111))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.power_supply_commands(port_cmd=False, output_on=False))

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 280, 81, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.power_supply_commands(port_cmd=True, connect_on=True))

        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 280, 81, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(lambda: self.power_supply_commands(port_cmd=True, connect_on=False))

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(110, 110, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(210, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(190, 280, 161, 21))
        self.label_4.setObjectName("label_4")

        self.retranslate_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    def retranslate_ui(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Power Supply Control"))
        self.pushButton.setText(_translate("Dialog", "On"))
        self.pushButton_2.setText(_translate("Dialog", "Off"))
        self.label.setText(_translate("Dialog", "Output"))
        self.label_2.setText(_translate("Dialog", "Channel 1 (A)"))
        self.label_3.setText(_translate("Dialog", "Channel 2 (A)"))
        self.pushButton_3.setText(_translate("Dialog", "Connect"))
        self.pushButton_4.setText(_translate("Dialog", "Disconnect"))
        self.label_4.setText(_translate("Dialog", "Disconnected from Power Supply"))
        self.textEdit.insertPlainText(_translate("Dialog", "0.000"))
        self.textEdit_2.insertPlainText(_translate("Dialog", "0.000"))

    def power_supply_commands(self, port_cmd=False, output_on=False, connect_on=False):
        if port_cmd:
            if connect_on:
                try:
                    UiDialog.rm = visa.ResourceManager()
                    UiDialog.ps = UiDialog.rm.open_resource(PowerSupplyCommands.ADDRESS)
                    UiDialog.ps.write(PowerSupplyCommands.COUPLE_ALL)
                    UiDialog.ps.write(PowerSupplyCommands.SET_VOLTAGE_1)
                    UiDialog.ps.write(PowerSupplyCommands.SET_VOLTAGE_2)
                    UiDialog.ps.write(PowerSupplyCommands.DISPLAY_CH2)
                except Exception as e:
                    print(e)
                else:
                    self.connected = True
                    self.label_4.setText('Connected to Power Supply')
            else:
                if self.connected:
                    try:
                        UiDialog.ps.close()
                        UiDialog.rm.close()
                    except Exception as e:
                        print(e)
                    else:
                        self.textEdit.insertPlainText('0.000')
                        self.textEdit_2.insertPlainText('0.000')
                        self.connected = False
                        self.label_4.setText('Disconnected from Power Supply')
                else:
                    pass
        else:
            if self.connected:
                if output_on:
                    try:
                        UiDialog.ps.write(PowerSupplyCommands.OUTPUT_ON)
                    except Exception as e:
                        print(e)
                else:
                    try:
                        UiDialog.ps.write(PowerSupplyCommands.OUTPUT_OFF)
                    except Exception as e:
                        print(e)
            else:
                pass

    def read_ps_current(self):
        if self.connected:
            
            self.textEdit.insertPlainText(str(self.ps.query(PowerSupplyCommands.GET_CURRENT_CH1)))
            self.textEdit.moveCursor(QTextCursor.End)
            self.textEdit_2.insertPlainText(str(self.ps.query(PowerSupplyCommands.GET_CURRENT_CH2)))
            self.textEdit_2.moveCursor(QTextCursor.End)
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = UiDialog()
    form.show()
    sys.exit(app.exec_())
