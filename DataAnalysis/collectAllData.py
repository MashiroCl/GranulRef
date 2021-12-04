from utils import dictAdd,RM_supported_type,getConfig
import glob,json,os

def makedir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def makeTxt(path):
    with open(path,"w") as f:
        f.close()

def makeCategory():
    path="/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/DataAnalysis/data/"
    project = "retrolambda"
    for i in range(2,5):
        makedir(path+project+str(i))
        makeTxt(path+project+str(i)+"/compareResult.txt")
        makeTxt(path + project + str(i) + "/time.txt")

def readCompareResult(path):
    with open(path) as f:
        lines = f.readlines()

    return json.loads(lines[4].split("they are")[1].replace('\'','\"'))

def addAll():
    data = getConfig()
    RMSupportedREF = data["local"]["RMSupportedREF"]
    dictSumAppear = RM_supported_type(RMSupportedREF)
    dictSumDisappear = RM_supported_type(RMSupportedREF)
    path="/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/DataAnalysis/data/"
    for file in glob.glob(path+"*/compareResult.txt"):
        # readCompareResult(file)
        dictAdd(dictSumAppear,readCompareResult(file))
    return dictSumAppear





if __name__ =="__main__":
    print(addAll())