'''个人数据数据处理'''

import json, os, shutil

# 配置文件
suitConfig_path = "src/suitConfig.json"
defaulCharacter_path = "src/character.json"
# 用户文件
folder = os.path.expanduser('~/Documents')
folder = folder + '/Genshin'
character_path = folder + '/character.json'
artifact_path = folder + '/artifacts.json'
artifactOwner_path = folder + '/artifactOwner.json'
artifactScheme_path = folder + "/artifactScheme.json"

# 数据常量
entryArray = ["暴击率", "暴击伤害", "攻击力", "生命值", "防御力", "元素精通", "元素充能效率"]
posName = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]
mainTagType = {
    "时之沙": ["生命值", "攻击力", "防御力", "元素精通", "元素充能效率"],
    "空之杯": ["生命值", "攻击力", "防御力", "元素精通", "物理伤害加成", "火元素伤害加成", "雷元素伤害加成",
               "水元素伤害加成", "草元素伤害加成", "风元素伤害加成", "岩元素伤害加成", "冰元素伤害加成"],
    "理之冠": ["生命值", "攻击力", "防御力", "元素精通", "暴击率", "暴击伤害", "治疗加成"],
}
combinationType = {
    "1+1+1+1+1": [
        ["C", "C", "C", "C", "C"]
    ],
    "4+1": [
        ["A", "A", "A", "A", "A"],
        ["C", "A", "A", "A", "A"],
        ["A", "C", "A", "A", "A"],
        ["A", "A", "C", "A", "A"],
        ["A", "A", "A", "C", "A"],
        ["A", "A", "A", "A", "C"]
    ],
    "2+2+1": [
        # 三个A两个B情况
        ["A", "A", "A", "B", "B"],
        ["A", "A", "B", "A", "B"],
        ["A", "A", "B", "B", "A"],
        ["A", "B", "A", "A", "B"],
        ["A", "B", "A", "B", "A"],
        ["A", "B", "B", "A", "A"],
        ["B", "A", "A", "A", "B"],
        ["B", "A", "A", "B", "A"],
        ["B", "A", "B", "A", "A"],
        ["B", "B", "A", "A", "A"],
        # 三个B两个A情况
        ["B", "B", "B", "A", "A"],
        ["B", "B", "A", "B", "A"],
        ["B", "B", "A", "A", "B"],
        ["B", "A", "B", "B", "A"],
        ["B", "A", "B", "A", "B"],
        ["B", "A", "A", "B", "B"],
        ["A", "B", "B", "B", "A"],
        ["A", "B", "B", "A", "B"],
        ["A", "B", "A", "B", "B"],
        ["A", "A", "B", "B", "B"],
        # 两个A两个B一个C情况
        ["C", "A", "A", "B", "B"],
        ["C", "A", "B", "A", "B"],
        ["C", "A", "B", "B", "A"],
        ["C", "B", "B", "A", "A"],
        ["C", "B", "A", "B", "A"],
        ["C", "B", "A", "A", "B"],
        ["A", "C", "A", "B", "B"],
        ["A", "C", "B", "A", "B"],
        ["A", "C", "B", "B", "A"],
        ["B", "C", "B", "A", "A"],
        ["B", "C", "A", "B", "A"],
        ["B", "C", "A", "A", "B"],
        ["A", "A", "C", "B", "B"],
        ["A", "B", "C", "A", "B"],
        ["A", "B", "C", "B", "A"],
        ["B", "B", "C", "A", "A"],
        ["B", "A", "C", "B", "A"],
        ["B", "A", "C", "A", "B"],
        ["A", "A", "B", "C", "B"],
        ["A", "B", "A", "C", "B"],
        ["A", "B", "B", "C", "A"],
        ["B", "B", "A", "C", "A"],
        ["B", "A", "B", "C", "A"],
        ["B", "A", "A", "C", "B"],
        ["B", "B", "A", "A", "C"],
        ["B", "A", "B", "A", "C"],
        ["B", "A", "A", "B", "C"],
        ["A", "A", "B", "B", "C"],
        ["A", "B", "A", "B", "C"],
        ["A", "B", "B", "A", "C"]
    ]
}
coefficient = {
    '暴击率': 2,
    '暴击伤害': 1,
    '攻击力百分比': 1.331429,
    '生命值百分比': 1.331429,
    '防御力百分比': 1.066362,
    '攻击力': 0.199146,
    '生命值': 0.012995,
    '防御力': 0.162676,
    '元素精通': 0.332857,
    '元素充能效率': 1.197943
}
average = {
    '暴击率': 3.3,
    '暴击伤害': 6.6,
    '攻击力百分比': 4.975,
    '生命值百分比': 4.975,
    '防御力百分比': 6.2,
    '攻击力': 16.75,
    '生命值': 254,
    '防御力': 19.75,
    '元素精通': 19.75,
    '元素充能效率': 5.5
}


class Data:
    def __init__(self):
        self.artifactList = {"生之花": {}, "死之羽": {}, "时之沙": {}, "空之杯": {}, "理之冠": {}}
        self.artifactOwnerList = {}
        self.suitConfig = {}
        self.characters = {}
        self.artifactScheme = {}
        # 加载数据
        self.loadData()

    def loadData(self):
        if os.path.exists(folder):
            # 读取圣遗物保存数据
            if os.path.exists(artifact_path):
                with open(artifact_path, 'r', encoding='utf-8') as fp:
                    self.artifactList = json.load(fp)
            # 读取圣遗物装备者保存数据
            if os.path.exists(artifactOwner_path):
                with open(artifactOwner_path, 'r', encoding='utf-8') as fp:
                    self.artifactOwnerList = json.load(fp)
            # 读取套装方案
            if os.path.exists(artifactScheme_path):
                with open(artifactScheme_path, 'r', encoding='utf-8') as fp:
                    self.artifactScheme = json.load(fp)
            # 读取角色参数配置
            if os.path.exists(character_path):
                with open(defaulCharacter_path, 'r', encoding='utf-8') as fp:
                    default = json.load(fp)
                with open(character_path, 'r', encoding='utf-8') as fp:
                    self.characters = json.load(fp)
                diff = default.keys() - self.characters.keys()
                if diff != set():
                    for item in diff:
                        self.characters[item] = default[item]
                    with open(character_path, 'w', encoding='utf-8') as fp:
                        json.dump(self.characters, fp, ensure_ascii=False)
            else:
                shutil.copy('src/character.json', character_path)
                with open(character_path, 'r', encoding='utf-8') as fp:
                    self.characters = json.load(fp)
        else:
            os.makedirs(folder)
            shutil.copy('src/character.json', character_path)
            with open(character_path, 'r', encoding='utf-8') as fp:
                self.characters = json.load(fp)

        with open(suitConfig_path, 'r', encoding='utf-8') as fp:
            self.suitConfig = json.load(fp)

    # 获取圣遗物套装配置
    def getSuitConfig(self):
        return self.suitConfig

    # 获取英雄配置
    def getCharacters(self):
        return self.characters

    def getArtifactList(self):
        return self.artifactList

    # 通过id获取英雄配置
    def getCharactersByCharacter(self, character):
        config = {}
        if character in self.characters:
            config = self.characters[character]
        return config

    # 更新英雄配置
    def setCharacters(self, newCharacters):
        self.characters = newCharacters
        with open(character_path, 'w', encoding='utf-8') as fp:
            json.dump(self.characters, fp, ensure_ascii=False)

    def getArtifactOwner(self, character):
        if character in self.artifactOwnerList:
            return self.artifactOwnerList[character]
        else:
            return {}

    # 通过角色名及装备列表替换装备
    def setArtifactOwner(self, character, newArtifactOwnerItem):
        for pos in newArtifactOwnerItem:
            ownerCharacter = self.getOwnerCharacterByArtifactId(pos, newArtifactOwnerItem[pos])
            if ownerCharacter:
                self.artifactOwnerList[ownerCharacter][pos] = "无装备"

        self.artifactOwnerList[character] = newArtifactOwnerItem

        # 保存数据
        with open(artifactOwner_path, 'w', encoding='utf-8') as fp:
            json.dump(self.artifactOwnerList, fp, ensure_ascii=False)

    # 通过ID及位置查询装备角色名称
    def getOwnerCharacterByArtifactId(self, pos, artifactID):
        for character in self.artifactOwnerList:
            if self.artifactOwnerList[character][pos] == artifactID:
                return character
        return None

    # 通过ID及位置查询装备
    def getArtifactItem(self, pos, artifactID):
        if pos in self.artifactList:
            if artifactID in self.artifactList[pos]:
                return self.artifactList[pos][artifactID]
            else:
                return {}
        else:
            return {}

    # 保存圣遗物
    def saveArtifactList(self, data):
        # 判断是否强化满级
        level = data[0][4]
        if level != '+20':
            print("未强化满级")
            return 0

        # 得分校验
        score = self.cal_score(data[1], self.getCharactersByCharacter("全属性"))[1]
        if score > 100:
            print("得分异常", score)
            return 0

        # 获取圣遗物ID
        nameArray = []
        nameArray.append(data[0][0])
        for itemName, itemNum in data[1].items():
            nameArray.append(str(itemNum))
        nameStr = '-'.join(nameArray)
        pos = data[0][1]

        if nameStr in self.artifactList[pos]:
            print("当前圣遗物已存在")
            return

        # 调整数据格式
        value = {}
        value["artifactName"] = data[0][0]
        value["pos"] = data[0][1]
        value["mainTag"] = data[0][2]
        value["normalTags"] = data[1]

        # 存储数据
        self.artifactList[pos][nameStr] = value
        with open(artifact_path, 'w', encoding='utf-8') as fp:
            json.dump(self.artifactList, fp, ensure_ascii=False)
            print("保存成功")

    def getCharacterIndex(self, character):
        resultIndex = 0
        if character in self.characters:
            characterKeyArray = list(self.characters.keys())
            resultIndex = characterKeyArray.index(character)
        return resultIndex

    # 推荐圣遗物
    def recommend(self, params):
        # 获取组合类型
        if params["suitA"] == "选择套装" and params["suitB"] == "选择套装":
            combinationKey = "1+1+1+1+1"
        elif params["suitA"] == "选择套装" and params["suitB"] != "选择套装":
            params["suitA"] = params["suitB"]
            combinationKey = "4+1"
        elif params["suitA"] != "选择套装" and params["suitB"] == "选择套装":
            combinationKey = "4+1"
        elif params["suitA"] != "选择套装" and params["suitB"] != "选择套装":
            if params["suitA"] == params["suitB"]:
                combinationKey = "4+1"
            else:
                combinationKey = "2+2+1"
        else:
            combinationKey = "1+1+1+1+1"

        # 筛选评分最大值套装
        suit = {
            "A": {},
            "B": {},
            "C": {},
        }
        for posItem in posName:
            array = {
                "A": [],
                "B": [],
                "C": [],
            }
            for artifactKey, artifactValue in self.artifactList[posItem].items():

                # 限制一 是否已装备
                if params["selectType"] == 1:
                    ownerCharacter = self.getOwnerCharacterByArtifactId(posItem, artifactKey)
                    if ownerCharacter and ownerCharacter != params["character"]:
                        # print("该装备已装备")
                        continue

                # 限制二 对比主词条
                if posItem in mainTagType:
                    # print(params["needMainTag"][posItem])
                    if artifactValue["mainTag"] not in params["needMainTag"][posItem]:
                        # print("主词条不符合")
                        continue

                # 开始筛选
                tempItem = {}
                tempItem["artifactID"] = artifactKey
                tempItem["artifactName"] = artifactValue["artifactName"]
                tempItem["score"] = self.cal_score(artifactValue["normalTags"], params["heroConfig"])[1]

                if combinationKey == "1+1+1+1+1":
                    array['C'].append(tempItem)
                elif combinationKey == "4+1":
                    if artifactValue["artifactName"] == self.suitConfig[params["suitA"]][posItem]:
                        array["A"].append(tempItem)
                    else:
                        array['C'].append(tempItem)
                elif combinationKey == "2+2+1":
                    if artifactValue["artifactName"] == self.suitConfig[params["suitA"]][posItem]:
                        array["A"].append(tempItem)
                    elif artifactValue["artifactName"] == self.suitConfig[params["suitB"]][posItem]:
                        array["B"].append(tempItem)
                    else:
                        array['C'].append(tempItem)

            # 取出当前位置最大值
            for suitKey in suit.keys():
                suit[suitKey][posItem] = 0
                if len(array[suitKey]) > 0:
                    array[suitKey].sort(key=lambda x: x["score"], reverse=True)
                    suit[suitKey][posItem] = array[suitKey][0]

        # print(suit)

        # 根据组合类型选出来总分最大组合
        scoreArray = []
        combination = combinationType[combinationKey]
        for combinationItem in combination:
            combinationName = {}
            tempFlag = 0
            scoreSum = 0
            for index in range(len(posName)):
                posItem = posName[index]
                combinationItemItem = combinationItem[index]
                if suit[combinationItemItem][posItem]:
                    scoreNum = suit[combinationItemItem][posItem]["score"]
                    combinationName[posItem] = suit[combinationItemItem][posItem]["artifactID"]
                    scoreSum += scoreNum
                else:
                    # print( posItem +" 不存在 计分中止1")
                    tempFlag = 1
                    break

            if tempFlag:
                # print("圣遗物不存在 计分中止2")
                continue
            scoreItem = {}
            scoreItem["combinationType"] = "".join(combinationItem)
            scoreItem["combinationName"] = combinationName
            scoreItem["scoreSum"] = round(scoreSum, 1)
            scoreArray.append(scoreItem)
        scoreArray.sort(key=lambda x: x["scoreSum"], reverse=True)
        # print(scoreArray)
        if len(scoreArray) > 0:
            return scoreArray
        else:
            return False

    def getIndexByCharacter(self, character):
        result = {"suitA": 0, "suitB": 0, "时之沙": [], "空之杯": [], "理之冠": []}
        if character in self.artifactScheme:
            artifactSchemeItem = self.artifactScheme[character]
            for key in artifactSchemeItem:
                if key == "suitA" or key == "suitB":
                    suitKeyArray = list(self.suitConfig.keys())
                    if artifactSchemeItem[key] in suitKeyArray:
                        result[key] = suitKeyArray.index(artifactSchemeItem[key]) + 1
                elif key in posName:
                    result[key] = artifactSchemeItem[key]
        return result

    def setArtifactScheme(self, character, params):
        self.artifactScheme[character] = params
        with open(artifactScheme_path, 'w', encoding='utf-8') as fp:
            json.dump(self.artifactScheme, fp, ensure_ascii=False)

    # 常量获取
    # 获取属性词条枚举
    def getEntryArray(self):
        return entryArray

    def getMainTagType(self):
        return mainTagType

    # 获取圣遗物位置名称
    def getPosName(self):
        return posName

    # 获取啥啊这是
    def getCoefficient(self):
        return coefficient

    # 获取配置文件夹路径
    def getUserDataPath(self):
        return folder

    def cal_score(self, ocr_result_sub, config):
        scores, sums, powerupArray, entriesSum = self.score(ocr_result_sub, config)
        return scores, sums, powerupArray, entriesSum

    def score2(self, ocr_result_sub, character="全属性"):
        config = self.characters[character]
        scores, sums, powerupArray, entriesSum = self.score(ocr_result_sub, config)
        return sums


    def score(self, ocr_result_sub, config):
        scores = []
        powerupArray = []
        sums = 0
        entriesSum = 0

        for key, value in ocr_result_sub.items():

            # 兼容角色配置未区分百分比的情况
            if key == '生命值百分比' or key == '攻击力百分比' or key == '防御力百分比':
                key_s = key[:3]
            else:
                key_s = key

            # key值存在误识别情况，则判定为0
            try:
                score = round(value * config[key_s] * coefficient[key], 1)
            except:
                score = 0
            scores.append(score)
            sums += score

            # 计算强化次数
            try:
                powerup = round(value / average[key]) - 1
            except:
                powerup = 0
            powerupArray.append(powerup)

            # 计算有效词条数量
            if key_s in config and config[key_s] > 0:
                entries = value / average[key]
                # print(key, entries)
                entriesSum += entries

        # print(scores, round(sums, 1), powerupArray, round(entriesSum, 1))
        return scores, round(sums, 1), powerupArray, round(entriesSum, 1)


    def checkUpdate(self):
        # 检查是否有装备可以更新
        result = []
        for owner in self.artifactOwnerList:
            scheme = self.artifactScheme[owner]

            params = {}
            params["suitA"] = scheme["suitA"]
            params["suitB"] = scheme["suitB"]
            params["needMainTag"] ={
                "时之沙": scheme["时之沙"],
                "空之杯": scheme["空之杯"],
                "理之冠": scheme["理之冠"],
            }
            params["character"] = owner
            params["heroConfig"] = self.characters[owner]
            params["selectType"] = 1
            recommendResult = self.recommend(params)

            if recommendResult:
                new = recommendResult[0]["combinationName"]
                old = self.artifactOwnerList[owner]
                for pos in posName:
                    if new[pos] != old[pos]:
                        result.append(owner)
                        break
            else:
                # 没有推荐结果
                print("没有推荐结果")
                pass
        return result
data = Data()
