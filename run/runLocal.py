import sys
sys.path.append('../')
from utils import step,getConfig,outputTime,timeRecord

def runLocal(repoPath,squashedOutput,clusterNum):
    data = getConfig()
    RMSupportedREF = data["local"]["RMSupportedREF"]
    RMPath = data["local"]["RMPath"]
    git_stein = data["local"]["git_stein"]
    recipe = data["local"]["recipe"]

    time_start = timeRecord()
    for num in range(clusterNum[0], clusterNum[1]):
        miaomiao = squashedOutput
        miaomiao += str(num)
        CompareResult = miaomiao + data["local"]["CompareResult"]
        step(RMPath=RMPath,repoPath=repoPath, recipe=recipe, git_stein=git_stein, squashedOutput=miaomiao, clusterNum=num,
             compareResult=CompareResult,RMSupportedREF=RMSupportedREF)

    time_end = timeRecord()
    t = time_end - time_start
    tResult = outputTime(t)
    print(tResult)
    timePath=data["local"]["time"]
    with open(timePath, "w") as f:
        f.writelines(tResult)

if __name__ =="__main__":
    temp="refactoring-toy-example"
    temp="mbassador"
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/"+temp
    output="/Users/leichen/ResearchAssistant/InteractiveRebase/data/experimentResult/"+temp
    clusterNum=[2,3]
    runLocal(repoPath,output,clusterNum)