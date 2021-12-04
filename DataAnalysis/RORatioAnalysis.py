import json

from utils import RM_supported_type, dictAdd


def readRO(filePath:str)->dict:
    with open(filePath) as f:
        data =f.read()
    data = data.replace("\'","\"")
    res = json.loads(data)
    return res

def calculateRatio():
    pass

if __name__ =="__main__":
    temp=["jbpm","jedis","refactoring-toy-example","retrolambda","RoboBinding"]

    RMSupportedREF = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/refactoringMiner/RMSupportedREF.txt"
    dictRO = RM_supported_type(RMSupportedREF)
    for each in temp:
        file = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/DataAnalysis/data/" \
               + each + "All/" + "RefactoringOperation.txt"
        res = readRO(file)
        print(res['change attribute access modifier'])
        dictRO = dictAdd(dictRO,res)
    print(dictRO)