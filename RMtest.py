from utils import dictAdd
from utils import RM_supported_type

def calcualte():
    a={'extract method': 8.5, 'inline method': 3.0, 'rename method': 20.0, 'move method': 19.0, 'move attribute': 2.5, 'pull up method': 20.5, 'pull up attribute': 8.5, 'push down method': 6.0, 'push down attribute': 2.5, 'extract superclass': 7.5, 'extract interface': 3.5, 'move class': 70.0, 'rename class': 12.5, 'extract and move method': 4.0, 'move and rename class': 4.0, 'extract class': 2.0, 'extract subclass': 1.5, 'extract variable': 1.0, 'rename variable': 33.0, 'rename parameter': 35.0, 'rename attribute': 6.5, 'change variable type': 30.5, 'change parameter type': 49.5, 'change return type': 38.0, 'change attribute type': 19.0, 'move and rename method': 5.0, 'add method annotation': 36.0, 'remove method annotation': 28.0, 'modify method annotation': 19.0, 'add class annotation': 1.5, 'modify class annotation': 1.0, 'add parameter': 17.0, 'remove parameter': 5.5, 'add thrown exception type': 3.0, 'remove thrown exception type': 5.0, 'change method access modifier': 13.5}
    b={'extract method': 16, 'inline method': 4, 'rename method': 26, 'move method': 29, 'move attribute': 11, 'pull up method': 20, 'pull up attribute': 5, 'push down method': 8, 'push down attribute': 3, 'extract superclass': 8, 'extract interface': 10, 'move class': 58, 'rename class': 23, 'extract and move method': 5, 'move and rename class': 14, 'extract class': 5, 'extract subclass': 1, 'extract variable': 8, 'inline variable': 1, 'rename variable': 43, 'rename parameter': 39, 'rename attribute': 15, 'replace variable with attribute': 2, 'change variable type': 87, 'change parameter type': 115, 'change return type': 70, 'change attribute type': 33, 'move and rename method': 4, 'add method annotation': 36, 'remove method annotation': 25, 'modify method annotation': 24, 'add class annotation': 13, 'modify class annotation': 2, 'add parameter': 16, 'remove parameter': 7, 'add thrown exception type': 3, 'remove thrown exception type': 5, 'change thrown exception type': 2, 'change method access modifier': 12}
    c={'move method': 1, 'move and rename class': 3, 'extract variable': 1}
    d={'extract method': 1, 'inline method': 1, 'rename method': 9, 'move method': 5, 'move attribute': 2, 'pull up method': 14, 'pull up attribute': 7, 'push down method': 2, 'push down attribute': 1, 'extract superclass': 2, 'extract interface': 1, 'move class': 28, 'rename class': 9, 'extract and move method': 1, 'move and rename class': 4, 'extract class': 1, 'extract subclass': 1, 'inline variable': 1, 'rename variable': 10, 'rename parameter': 7, 'change variable type': 11, 'change parameter type': 12, 'change return type': 23, 'change attribute type': 11, 'move and rename method': 4, 'add method annotation': 17, 'remove method annotation': 14, 'modify method annotation': 16, 'add parameter': 6, 'remove parameter': 3, 'add thrown exception type': 2, 'remove thrown exception type': 2, 'change method access modifier': 11}

    temp1,temp2,temp3,temp4=RM_supported_type(),RM_supported_type(),RM_supported_type(),RM_supported_type()
    temp1=dictAdd(temp1, a)
    temp2=dictAdd(temp2, b)
    temp3=dictAdd(temp3, c)
    temp4=dictAdd(temp4, d)

    n=[0]*4
    for each in temp1:
        if temp1[each]!=temp2[each]-temp3[each]+temp4[each]:
            print(each)
        n[0] += temp1[each]
        n[1] += temp2[each]
        n[2] += temp3[each]
        n[3] += temp4[each]

    print(n)

import os
def squashTest():
    git_stein = "/Users/leichen/Code/git-stein/build/libs/git-stein-all.jar"
    recipe = "./recipe.json"
    output = "/Users/leichen/Desktop/RTEnew/"
    temp ="retrolambda"
    # temp = "jfinal"
    repository  = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/"+temp

    commits = "[['c32db1a20e5b81133f8980360931eec02749215e', 'b8c4575280d9182be93dd62853c5e3afb6b6e520'], ['b681452ccbe11fb19db433c95fa7a2236796b4c8', 'a8b857c28a85c0bd6460accf8326bedb7c8f19b6'], ['8be3092acf40c2f4c8f2e85cf6319508e2e17551', '28341bbed6f6210ed12cc9f1af84ca21919a2c31'], ['40985c0c0f5ac4874095a8b28532464e6a8800fd', 'e4a889a1ee31f1c1fddcc1c5a71cd3073cecf5d8'], ['152cc18d32a4c383d9fa612881f2b96c32635082', 'e62479c6cae97cb3404323389d6ef8a18d750514'], ['a7588bbb99991bdc46097f6685b2dbb4e7ff1dc1', 'f5807dec9c1488d52a1bb0a8ec15a83ce6adc7ec'], ['92a4a83ac6e7c05bc3b263debf75516658691bc2', 'be8c3b3d4f4cf330f1417dd7a231939107042f93'], ['e2f7ad16cd5fb4e22c3b9fc8cdfb48d667bab0f9', 'ec3c55b307ed1738202459decd9026dbbdd009f0'], ['29e14b2f72bee225d20c94fbf3f72c570fcbcf65', '101e1146d62b78beb0aa07285c1d3caf391ada5c'], ['d957c3c8b6761ca53703a6074b033eb0843d2dde', '1b7f8ba25482a74522474b50e78136ee17cd5e64']]"
    # commits = "[['4bf9a7f76d727db0b69a986de683dd466991899b', 'aa0cadbe721f638855837e8ea3dea2c6b9c34415']]"
    recipeContents = '{"forcedClusters":'+commits.replace("\'","\"")+' }'
    with open(recipe,"w") as f:
        f.write(recipeContents)
    command = "java -jar " + git_stein + " Clusterer " + "--recipe=" + recipe + " -v -o " + output + " " + repository + ">" + "./stein.log"
    print(command)
    os.system(command)

    'Find newly generated commit No.'
    with open("./stein.log","r") as f:
        lines=f.readlines()
    result=[]
    commits = [['c32db1a20e5b81133f8980360931eec02749215e', 'b8c4575280d9182be93dd62853c5e3afb6b6e520'], ['b681452ccbe11fb19db433c95fa7a2236796b4c8', 'a8b857c28a85c0bd6460accf8326bedb7c8f19b6'], ['8be3092acf40c2f4c8f2e85cf6319508e2e17551', '28341bbed6f6210ed12cc9f1af84ca21919a2c31'], ['40985c0c0f5ac4874095a8b28532464e6a8800fd', 'e4a889a1ee31f1c1fddcc1c5a71cd3073cecf5d8'], ['152cc18d32a4c383d9fa612881f2b96c32635082', 'e62479c6cae97cb3404323389d6ef8a18d750514'], ['a7588bbb99991bdc46097f6685b2dbb4e7ff1dc1', 'f5807dec9c1488d52a1bb0a8ec15a83ce6adc7ec'], ['92a4a83ac6e7c05bc3b263debf75516658691bc2', 'be8c3b3d4f4cf330f1417dd7a231939107042f93'], ['e2f7ad16cd5fb4e22c3b9fc8cdfb48d667bab0f9', 'ec3c55b307ed1738202459decd9026dbbdd009f0'], ['29e14b2f72bee225d20c94fbf3f72c570fcbcf65', '101e1146d62b78beb0aa07285c1d3caf391ada5c'], ['d957c3c8b6761ca53703a6074b033eb0843d2dde', '1b7f8ba25482a74522474b50e78136ee17cd5e64']]
    for eachList in commits:
        for eachLine in lines:
            if " Rewrite commit: " in eachLine:
                temp = eachLine.split("Rewrite commit: ")[1].split(" -> ")
                'Attention: merge not excluded'
                if temp[0].strip() == eachList[0].strip():
                    result.append(temp[1].strip())
    print(result)

if __name__ == "__main__":
    squashTest()
    # test = "Rewrite commit: c32db1a20e5b81133f8980360931eec02749215e -> 94e8e4b563528ebc9832d5cc687c9e2271a8e8e0"
    # temp = test.split("Rewrite commit: ")[1].split(" -> ")
    # # eachList = ['c32db1a20e5b81133f8980360931eec02749215e', 'b8c4575280d9182be93dd62853c5e3afb6b6e520']
    # result = []
    # commits = "[['c32db1a20e5b81133f8980360931eec02749215e', 'b8c4575280d9182be93dd62853c5e3afb6b6e520'], ['b681452ccbe11fb19db433c95fa7a2236796b4c8', 'a8b857c28a85c0bd6460accf8326bedb7c8f19b6'], ['8be3092acf40c2f4c8f2e85cf6319508e2e17551', '28341bbed6f6210ed12cc9f1af84ca21919a2c31'], ['40985c0c0f5ac4874095a8b28532464e6a8800fd', 'e4a889a1ee31f1c1fddcc1c5a71cd3073cecf5d8'], ['152cc18d32a4c383d9fa612881f2b96c32635082', 'e62479c6cae97cb3404323389d6ef8a18d750514'], ['a7588bbb99991bdc46097f6685b2dbb4e7ff1dc1', 'f5807dec9c1488d52a1bb0a8ec15a83ce6adc7ec'], ['92a4a83ac6e7c05bc3b263debf75516658691bc2', 'be8c3b3d4f4cf330f1417dd7a231939107042f93'], ['e2f7ad16cd5fb4e22c3b9fc8cdfb48d667bab0f9', 'ec3c55b307ed1738202459decd9026dbbdd009f0'], ['29e14b2f72bee225d20c94fbf3f72c570fcbcf65', '101e1146d62b78beb0aa07285c1d3caf391ada5c'], ['d957c3c8b6761ca53703a6074b033eb0843d2dde', '1b7f8ba25482a74522474b50e78136ee17cd5e64']]"
    #
    # if temp[0].strip() == eachList[0].strip():
    #     result.append(temp[1].strip())
    # print(result)
