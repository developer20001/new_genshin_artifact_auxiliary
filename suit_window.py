'''圣遗物推荐参数选择弹窗'''

import os
from data import data
from extention import ExtendedComboBox

from suit_result_window import SuitResultWindow
from set_window import SetWindow


from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QRadioButton,
    QPushButton,
    QWidget,
    QGridLayout
)


class SuitWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'src/keqing.ico')))
        self.setWindowTitle("圣遗物套装推荐")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(0, 0)

        # 初始化子窗口
        self.setWindow = None
        self.suitResultWindow = None

        # 初始化变量
        self.suitProgrammeWindow = None
        self.character = "全属性"
        self.selectType = 1

        # 创建界面UI
        self.openFileButton = QPushButton('打开文件')
        self.dataUpdateButton = QPushButton('更新数据')
        self.mainButton = QPushButton('圣遗物评分→')
        self.heroNameCombobox = ExtendedComboBox()
        for herName in data.getCharacters():
            self.heroNameCombobox.addItem(herName)
        self.setButton = QPushButton('设置>')
        self.suitCombobox1 = ExtendedComboBox()
        self.suitCombobox2 = ExtendedComboBox()
        self.suitCombobox1.addItem("选择套装")
        self.suitCombobox2.addItem("选择套装")
        for key in data.getSuitConfig():
            self.suitCombobox1.addItem(key)
            self.suitCombobox2.addItem(key)
        self.mainTagTips = QLabel('(必选！！！)')
        self.mainTagTips.setStyleSheet("color:red;")
        self.mainTagNameArray = []
        self.mainTagComboboxArray = []
        MainTagType = data.getMainTagType()
        for key in MainTagType:
            mainTagName = QLabel(key)
            mainTagCombobox = ExtendedComboBox()
            mainTagCombobox.addItem("主属性选择")
            for tagItem in MainTagType[key]:
                mainTagCombobox.addItem(tagItem)
            self.mainTagNameArray.append(mainTagName)
            self.mainTagComboboxArray.append(mainTagCombobox)
        self.radiobtn1 = QRadioButton('仅未装备')
        self.radiobtn1.setChecked(True)
        self.radiobtn2 = QRadioButton('全部')
        self.startButton = QPushButton('生成方案')
        # self.tipsLabel = QLabel('主要属性为必选项！！！')
        # self.tipsLabel.setStyleSheet("color:red;qproperty-alignment: 'AlignCenter';")

        # 弹窗内容
        layout = QGridLayout()
        layout.addWidget(self.openFileButton, 0, 0, 1, 1)
        layout.addWidget(self.dataUpdateButton, 0, 1, 1, 1)
        layout.addWidget(self.mainButton, 0, 2, 1, 2)
        layout.addWidget(QLabel('当前角色：'), 1, 0, 1, 1)
        layout.addWidget(self.heroNameCombobox, 1, 1, 1, 2)
        layout.addWidget(self.setButton, 1, 3, 1, 1)
        layout.addWidget(QLabel('套装类型:'), 2, 0, 1, 1)
        layout.addWidget(QLabel('套装A'), 3, 1, 1, 1)
        layout.addWidget(self.suitCombobox1, 3, 2, 1, 2)
        layout.addWidget(QLabel('套装B'), 4, 1, 1, 1)
        layout.addWidget(self.suitCombobox2, 4, 2, 1, 2)
        layout.addWidget(QLabel('主要属性:'), 5, 0, 1, 1)
        layout.addWidget(self.mainTagTips, 5, 1, 1, 4)
        for index in range(len(self.mainTagComboboxArray)):
            layout.addWidget(self.mainTagNameArray[index], 6 + index, 1, 1, 2)
            layout.addWidget(self.mainTagComboboxArray[index], 6 + index, 2, 1, 2)
        layout.addWidget(QLabel('其他选择:'), 9, 0, 1, 1)
        layout.addWidget(self.radiobtn1, 10, 1, 1, 1)
        layout.addWidget(self.radiobtn2, 10, 2, 1, 1)
        layout.addWidget(self.startButton, 11, 0, 1, 4)
        # layout.addWidget(self.tipsLabel, 12, 0, 1, 4)
        self.setLayout(layout)

        # 注册事件
        self.openFileButton.clicked.connect(self.openFile)
        self.dataUpdateButton.clicked.connect(self.updateData)
        self.mainButton.clicked.connect(self.swichMainWindow)
        self.heroNameCombobox.currentIndexChanged.connect(self.heroNameCurrentIndexChanged)
        self.radiobtn1.toggled.connect(lambda: self.radiobtn_state(self.radiobtn1))
        self.radiobtn2.toggled.connect(lambda: self.radiobtn_state(self.radiobtn2))
        self.startButton.clicked.connect(self.startRating)
        self.setButton.clicked.connect(self.openSetWindow)

    def closeEvent(self, event):
        # print("关闭窗口")
        if self.setWindow:
            self.setWindow.close()
        if self.suitResultWindow:
            self.suitResultWindow.close()

    # 自定义方法
    def startRating(self):
        needMainTag = {"生之花": "生命值", "死之羽": "攻击力"}
        for index in range(len(self.mainTagNameArray)):
            mainTagKey = self.mainTagNameArray[index].text()
            mainTag = self.mainTagComboboxArray[index].currentText()
            if mainTag == "主属性选择":
                self.mainTagTips.setText(mainTagKey.replace(":", " ") + "主要属性未选择！！！")
                return 0
            needMainTag[mainTagKey] = mainTag

        params = {}
        params["character"] = self.character
        params["heroConfig"] = data.getCharacters()[self.character]
        params["suit1"] = self.suitCombobox1.currentText()
        params["suit2"] = self.suitCombobox2.currentText()
        params["needMainTag"] = needMainTag
        params["selectType"] = self.selectType

        # 获取推荐数据
        result = data.recommend(params)
        if result:
            self.mainTagTips.setText("(必选！！！)")
            self.suitResultWindow = SuitResultWindow()
            self.suitResultWindow.update(self.character, result)
            self.suitResultWindow.show()
        else:
            self.mainTagTips.setText("没有合适的方案！！！")

    # 单选框按钮
    def radiobtn_state(self, btn):
        if btn.text() == '仅未装备' and btn.isChecked() == True:
            self.selectType = 1
        elif btn.text() == '全部' and btn.isChecked() == True:
            self.selectType = 2

    # 英雄名称
    def heroNameCurrentIndexChanged(self):
        self.character = self.heroNameCombobox.currentText()
        if self.setWindow:
            self.setWindow.update(self.character)

    # 设置按钮
    def updateData(self):
        data.loadData()

    # 打开文件夹
    def openFile(self):
        os.startfile(data.folder)

    #切换为评分
    def swichMainWindow(self):
        from app import MainWindow
        window = MainWindow()
        window.show()
        self.close()

    def openSetWindow(self):
        self.setWindow = SetWindow()
        self.setWindow.update(self.character)
        self.setWindow.show()