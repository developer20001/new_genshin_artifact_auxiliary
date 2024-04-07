'''个人数据数据处理'''

import json, os, shutil
import score

# 路径常量
folder = os.path.expanduser('~/Documents')
folder = folder + '/keqing'
character_path = folder + '/character.json'
artifact_path = folder + '/artifacts.json'
artifactOwner_path = folder + '/artifactOwner.json'
suitConfig_path = "src/suitConfig.json"
archive_path = folder + '/archive.json'

# 数据常量
posName = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]
mainTagType = {
    "时之沙": ["生命值", "攻击力", "防御力", "元素精通", "元素充能效率"],
    "空之杯": ["生命值", "攻击力", "防御力", "元素精通", "物理伤害加成", "火元素伤害加成", "雷元素伤害加成",
               "水元素伤害加成", "草元素伤害加成", "风元素伤害加成", "岩元素伤害加成", "冰元素伤害加成"],
    "理之冠": ["生命值", "攻击力", "防御力", "元素精通", "暴击率", "暴击伤害", "治疗加成"],
}
combinationType = {
    "5": [
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

# 数据默认值
artifacts = {'背包': {}, '角色': {}}
artifactList = {"生之花": {}, "死之羽": {}, "时之沙": {}, "空之杯": {}, "理之冠": {}}
artifactOwnerList = {}
suitConfig = {}
characters = {}




# 数据创建或者读取
def loadData():
    # 将数据进行全局声明
    global artifactList
    global artifactOwnerList
    global characters
    global artifacts
    global suitConfig

    if os.path.exists(folder):
        # 读取圣遗物保存数据
        if os.path.exists(artifact_path):
            with open(artifact_path, 'r', encoding='utf-8') as fp:
                artifactList = json.load(fp)
        # 读取圣遗物装备者保存数据
        if os.path.exists(artifactOwner_path):
            with open(artifactOwner_path, 'r', encoding='utf-8') as fp:
                artifactOwnerList = json.load(fp)
        # 读取角色参数配置
        if os.path.exists(character_path):
            with open('src/character.json', 'r', encoding='utf-8') as fp:
                default = json.load(fp)
            with open(character_path, 'r', encoding='utf-8') as fp:
                characters = json.load(fp)
            diff = default.keys() - characters.keys()
            if diff != set():
                for item in diff:
                    characters[item] = default[item]
                with open(character_path, 'w', encoding='utf-8') as fp:
                    json.dump(characters, fp, ensure_ascii=False)
        else:
            shutil.copy('src/character.json', character_path)
            with open(character_path, 'r', encoding='utf-8') as fp:
                characters = json.load(fp)
        # 读取保存数据
        if os.path.exists(archive_path):
            with open(archive_path, 'r', encoding='utf-8') as fp:
                artifacts = json.load(fp)
    else:
        os.makedirs(folder)
        shutil.copy('src/character.json', character_path)
        with open(character_path, 'r', encoding='utf-8') as fp:
            characters = json.load(fp)

    with open(suitConfig_path, 'r', encoding='utf-8') as fp:
        suitConfig = json.load(fp)


loadData()


# 获取保存的数据
def getArtifacts():
    return artifacts


def setArtifacts(newArtifacts):
    global artifacts
    artifacts = newArtifacts
    with open(archive_path, 'w', encoding='utf-8') as fp:
        json.dump(artifacts, fp, ensure_ascii=False)


# 获取圣遗物套装配置
def getSuitConfig():
    return suitConfig


# 获取圣遗物类型配置
def getMainTagType():
    return mainTagType


# 获取英雄配置
def getCharacters():
    return characters


def getCharactersByCharacter(character):
    config = {}
    if character in characters:
        config = characters[character]
    return config


# 更新英雄配置
def setCharacters(newCharacters):
    global characters
    characters = newCharacters
    with open(character_path, 'w', encoding='utf-8') as fp:
        json.dump(characters, fp, ensure_ascii=False)


# 获取圣遗物位置名称
def getPosName():
    return posName


def getArtifactOwner(character):
    if character in artifactOwnerList:
        return artifactOwnerList[character]
    else:
        return {}


# 通过角色名及装备列表替换装备
def setArtifactOwner(character, newArtifactOwnerItem):
    for pos in newArtifactOwnerItem:
        ownerCharacter = getOwnerCharacterByArtifactId(pos, newArtifactOwnerItem[pos])
        if ownerCharacter:
            artifactOwnerList[ownerCharacter][pos] = "无装备"

    artifactOwnerList[character] = newArtifactOwnerItem

    # 保存数据
    with open(artifactOwner_path, 'w', encoding='utf-8') as fp:
        json.dump(artifactOwnerList, fp, ensure_ascii=False)


# 通过ID及位置查询装备
def getArtifactItem(pos, artifactID):
    if pos in artifactList:
        if artifactID in artifactList[pos]:
            return artifactList[pos][artifactID]
        else:
            return {}
    else:
        return {}


# 通过ID及位置查询装备角色名称
def getOwnerCharacterByArtifactId(pos, artifactID):
    for character in artifactOwnerList:
        if artifactOwnerList[character][pos] == artifactID:
            return character
    return None


# 保存圣遗物
def saveArtifactList(data):
    # 判断是否强化满级
    level = data[0][4]
    if level != '+20':
        print("未强化满级")
        return 0

    # 获取圣遗物ID
    nameArray = []
    nameArray.append(data[0][0])
    for itemName, itemNum in data[1].items():
        nameArray.append(str(itemNum))
    nameStr = '-'.join(nameArray)
    pos = data[0][1]

    if nameStr in artifactList[pos]:
        print("当前圣遗物已存在")
        return

    # 调整数据格式
    value = {}
    value["artifactName"] = data[0][0]
    value["pos"] = data[0][1]
    value["mainTag"] = data[0][2]
    value["normalTags"] = data[1]

    # 存储数据
    artifactList[pos][nameStr] = value
    with open(artifact_path, 'w', encoding='utf-8') as fp:
        json.dump(artifactList, fp, ensure_ascii=False)
        print("保存成功")


# 推荐圣遗物
def recommend(params):
    # 获取组合类型
    if params["suit1"] == "选择套装" and params["suit2"] == "选择套装":
        combinationKey = "5"
    elif params["suit1"] == "选择套装" and params["suit2"] != "选择套装":
        params["suit1"] = params["suit2"]
        combinationKey = "4+1"
    elif params["suit1"] != "选择套装" and params["suit2"] == "选择套装":
        combinationKey = "4+1"
    elif params["suit1"] != "选择套装" and params["suit2"] != "选择套装":
        if params["suit1"] == params["suit2"]:
            combinationKey = "4+1"
        else:
            combinationKey = "2+2+1"
    else:
        combinationKey = "5"

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
        for artifactKey, artifactValue in artifactList[posItem].items():

            # 限制一 是否已装备
            if params["selectType"] == 1:
                ownerCharacter = getOwnerCharacterByArtifactId(posItem, artifactKey)
                if ownerCharacter and ownerCharacter != params["character"]:
                    print("该装备已装备")
                    continue

            # 限制二 对比主词条
            if artifactValue["mainTag"] != params["needMainTag"][posItem]:
                # print("主词条不符合")
                continue

            # 开始筛选
            tempItem = {}
            tempItem["artifactID"] = artifactKey
            tempItem["artifactName"] = artifactValue["artifactName"]
            tempItem["score"] = score.cal_score(artifactValue["normalTags"], params["heroConfig"])[1]

            if combinationKey == "5":
                array['C'].append(tempItem)
            elif combinationKey == "4+1":
                if artifactValue["artifactName"] == suitConfig[params["suit1"]][posItem]:
                    array["A"].append(tempItem)
                else:
                    array['C'].append(tempItem)
            elif combinationKey == "2+2+1":
                if artifactValue["artifactName"] == suitConfig[params["suit1"]][posItem]:
                    array["A"].append(tempItem)
                elif artifactValue["artifactName"] == suitConfig[params["suit2"]][posItem]:
                    array["B"].append(tempItem)
                else:
                    array['C'].append(tempItem)

        # 取出当前位置最大值
        for suitKey in suit.keys():
            suit[suitKey][posItem] = 0
            if len(array[suitKey]) > 0:
                array[suitKey].sort(key=lambda x: x["score"], reverse=True)
                suit[suitKey][posItem] = array[suitKey][0]

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
                # print( posItem +" 圣遗物不存在 计分中止1")
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
    print(scoreArray)
    if len(scoreArray) > 0:
        return scoreArray
    else:
        return 0
