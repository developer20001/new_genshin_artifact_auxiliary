'''设置窗口，自定义词条收益权重'''

import os
from data import data
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout,
    QDoubleSpinBox
)

class SetWindow(QWidget):

    statusSignal = Signal(object)

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'src/keqing.ico')))
        self.setWindowTitle("得分权重设置")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(340, 0)

        # 初始化数值
        self.character = ""
        self.config = {}

        # 显示当前角色
        self.heroNameLabel1 = QLabel('当前角色：')
        self.heroNameLabel2 = QLabel("")

        # 显示得分权重
        self.entryName = []
        self.entryNum = []
        for keyName in data.getEntryArray():
            nameText = QLabel(keyName)
            self.entryName.append(nameText)

            numText = QDoubleSpinBox()
            numText.setMinimum(0)
            numText.setMaximum(1)
            numText.setSingleStep(0.1)
            numText.setValue(0)
            numText.setAlignment(Qt.AlignRight)
            self.entryNum.append(numText)

        # 添加保存按钮
        self.saveButton = QPushButton('确认修改')

        # 注意事项
        self.tipsLabel1 = QLabel('注意事项：')
        self.tipsLabel1.setStyleSheet("color:red;")
        self.tipsLabel2 = QLabel('1.小词条（固定值）得分为大词条（百分比）的一半')
        self.tipsLabel2.setStyleSheet("color:red;")

        # 弹窗内容
        layout = QGridLayout()
        layout.addWidget(self.heroNameLabel1, 1, 1)
        layout.addWidget(self.heroNameLabel2, 1, 2)
        for index in range(len(self.entryName)):
            layout.addWidget(self.entryName[index],index+2,1)
        for index in range(len(self.entryNum)):
            layout.addWidget(self.entryNum[index], index+2,2)
        layout.addWidget(self.saveButton, 9, 1, 1, 2)
        layout.addWidget(self.tipsLabel1, 10, 1, 1, 2)
        layout.addWidget(self.tipsLabel2, 11, 1, 1, 2)
        self.setLayout(layout)

        # 注册按钮事件
        self.saveButton.clicked.connect(self.btn_save)

    def update(self,character):
        self.character = character
        self.updateUI()

    def updateUI(self):
        herConfig = data.getCharacters()
        entryArray = data.getEntryArray()
        # 兼容数据异常情况
        if not self.character in herConfig or herConfig[self.character]=={}:
            self.heroNameLabel2.setText("请正确的选择角色")
            for index in range(len(entryArray)):
                self.entryNum[index].setValue(0)
        else:
            self.heroNameLabel2.setText(self.character)
            for index in range(len(entryArray)):
                self.entryNum[index].setValue(herConfig[self.character][entryArray[index]])


    def btn_save(self):
        herConfig = data.getCharacters()
        tempConfig = {}
        for index in  range(len(self.entryNum)):
            tempConfig[self.entryName[index].text()] = self.entryNum[index].value()
        herConfig[self.character] = tempConfig
        data.setCharacters(herConfig)
        self.close()