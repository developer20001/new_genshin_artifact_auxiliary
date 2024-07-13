'''圣遗物推荐参数选择弹窗'''

import os, copy
from data import data
from extention import ExtendedComboBox, XCombobox

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
        self.checkButton = QPushButton('检查更新')

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
        self.mainTagCombobox = {}
        MainTagType = data.getMainTagType()
        for key in MainTagType:
            mainTagCombobox = XCombobox("任意属性")
            mainTagCombobox.add_items(MainTagType[key])
            self.mainTagCombobox[key] = mainTagCombobox
        self.radiobtn1 = QRadioButton('仅未装备')
        self.radiobtn1.setChecked(True)
        self.radiobtn2 = QRadioButton('全部')
        self.startButton = QPushButton('生成方案')
        self.tipsText = QLabel('提示文本')

        # 弹窗内容
        layout = QGridLayout()
        layout.addWidget(self.openFileButton, 0, 0, 1, 1)
        layout.addWidget(self.dataUpdateButton, 0, 1, 1, 1)
        layout.addWidget(self.mainButton, 0, 2, 1, 2)
        layout.addWidget(self.checkButton, 1, 0, 1, 4)

        layout.addWidget(QLabel('当前角色：'), 11, 0, 1, 1)
        layout.addWidget(self.heroNameCombobox, 11, 1, 1, 2)
        layout.addWidget(self.setButton, 11, 3, 1, 1)
        layout.addWidget(QLabel('套装类型:'), 12, 0, 1, 1)
        # layout.addWidget(QLabel('(选一个4+1,选两个2+2+1,不选散搭)'), 2, 1, 1, 4)
        layout.addWidget(QLabel('套装A'), 13, 1, 1, 1)
        layout.addWidget(self.suitCombobox1, 13, 2, 1, 2)
        layout.addWidget(QLabel('套装B'), 14, 1, 1, 1)
        layout.addWidget(self.suitCombobox2, 14, 2, 1, 2)
        layout.addWidget(QLabel('主要属性:'), 15, 0, 1, 1)
        layout.addWidget(QLabel('(不选默认不限制主词条)'), 15, 1, 1, 4)
        index = 0
        for key in self.mainTagCombobox:
            layout.addWidget(QLabel(key), 16 + index, 1, 1, 2)
            layout.addWidget(self.mainTagCombobox[key], 16 + index, 2, 1, 2)
            index += 1
        layout.addWidget(QLabel('其他选择:'), 19, 0, 1, 1)
        layout.addWidget(self.radiobtn1, 20, 1, 1, 1)
        layout.addWidget(self.radiobtn2, 20, 2, 1, 1)
        layout.addWidget(self.startButton, 21, 0, 1, 4)
        layout.addWidget(self.tipsText, 22, 0, 1, 4, Qt.AlignCenter)

        self.setLayout(layout)

        self.updateUI()

        # 注册事件
        self.openFileButton.clicked.connect(self.openFile)
        self.dataUpdateButton.clicked.connect(self.updateData)
        self.mainButton.clicked.connect(self.swichMainWindow)
        self.heroNameCombobox.currentIndexChanged.connect(self.heroNameCurrentIndexChanged)
        self.radiobtn1.toggled.connect(lambda: self.radiobtn_state(self.radiobtn1))
        self.radiobtn2.toggled.connect(lambda: self.radiobtn_state(self.radiobtn2))
        self.startButton.clicked.connect(self.startRating)
        self.setButton.clicked.connect(self.openSetWindow)
        self.checkButton.clicked.connect(self.checkButtonClicked)

    def closeEvent(self, event):
        # print("关闭窗口")
        if self.setWindow:
            self.setWindow.close()
        if self.suitResultWindow:
            self.suitResultWindow.close()

    # 自定义方法
    def startRating(self):

        params = {}
        params["suitA"] = self.suitCombobox1.currentText()
        params["suitB"] = self.suitCombobox2.currentText()
        needMainTag = {}
        for key in self.mainTagCombobox:
            mainTag = self.mainTagCombobox[key].get_selected()
            needMainTag[key] = mainTag
            params[key] = mainTag

        # 保存方案
        saveParams = copy.deepcopy(params)
        data.setArtifactScheme(self.character, saveParams)

        params["needMainTag"] = needMainTag
        params["character"] = self.character
        params["heroConfig"] = data.getCharacters()[self.character]
        params["selectType"] = self.selectType

        # 获取推荐数据
        result = data.recommend(params)
        if result:
            self.suitResultWindow = SuitResultWindow()
            self.suitResultWindow.update(self.character, result)
            self.suitResultWindow.show()
        else:
            print("无可用方案")

    # 单选框按钮
    def radiobtn_state(self, btn):
        if btn.text() == '仅未装备' and btn.isChecked() == True:
            self.selectType = 1
        elif btn.text() == '全部' and btn.isChecked() == True:
            self.selectType = 2

    def initUI(self, character):
        index = data.getCharacterIndex(character)
        self.heroNameCombobox.setCurrentIndex(index)
        self.updateUI()


    def updateUI(self):
        indexObj = data.getIndexByCharacter(self.character)
        for key in indexObj:
            if key == "suitA":
                self.suitCombobox1.setCurrentIndex(indexObj[key])
            elif key == "suitB":
                self.suitCombobox2.setCurrentIndex(indexObj[key])
            else:
                if key in self.mainTagCombobox:
                    self.mainTagCombobox[key].set_selected(indexObj[key])

    # 英雄名称
    def heroNameCurrentIndexChanged(self):
        self.character = self.heroNameCombobox.currentText()
        if self.setWindow:
            self.setWindow.update(self.character)
        self.updateUI()

    # 设置按钮
    def updateData(self):
        data.loadData()

    # 打开文件夹
    def openFile(self):
        os.startfile(data.getUserDataPath())

    # 切换为评分
    def swichMainWindow(self):
        from app import MainWindow
        window = MainWindow()
        window.initCombobox(self.character)
        window.show()
        self.close()


    def openSetWindow(self):
        self.setWindow = SetWindow()
        self.setWindow.update(self.character)
        self.setWindow.show()


    def checkButtonClicked(self):
        updateArray = data.checkUpdate()

        print(updateArray)
        tipsStr = ""
        if len(updateArray)>0:
            tipsStr = "、".join(updateArray)+" 需要更新"
        else:
            tipsStr = "没有需要更新的套装"
        self.tipsText.setText(tipsStr)