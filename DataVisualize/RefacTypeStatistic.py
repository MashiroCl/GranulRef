def getRefacTypeStatistic(filePath):
    with open(filePath,"r") as f:
        lines = f.readlines()
    for each in lines:
        if each.startswith("Number of RO generated because of squash is"):
            strDict = each.split("they are")[1]
            generated= eval(strDict)

        if each.startswith("Number of RO disappear because of squash is"):
            strDict = each.split("they are")[1]
            disappear = eval(strDict)
    return generated,disappear



if __name__=="__main__":
    RMSpath="../RMSupportedREF.txt"
    # print(RM_supported_type(RMSpath))
    filePath="/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/DataVisualize/compareResult2.txt"
    gRT,dRT = getRefacTypeStatistic(filePath)
    gRT=sorted(gRT.items(),key=lambda num:num[1],reverse=True)
    dRT = sorted(dRT.items(), key=lambda num: num[1], reverse=True)
    print(gRT)
    print(dRT)
