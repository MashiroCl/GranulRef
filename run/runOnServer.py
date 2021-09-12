import sys
sys.path.append('../')
from utils import outputTime,step,getConfig,timeRecord

def runServer(repoPath,squashedOutput,clusterNum):
    data = getConfig()
    RMSupportedREF = data["titan"]["RMSupportedREF"]
    RMPath = data["titan"]["RMPath"]
    git_stein = data["titan"]["git_stein"]
    recipe = data["titan"]["recipe"]

    for num in range(clusterNum[0], clusterNum[1]):
        time_start = timeRecord()
        outputName = squashedOutput
        outputName += str(num)
        CompareResult = outputName + data["titan"]["CompareResult"]
        step(RMPath=RMPath,repoPath=repoPath, recipe=recipe, git_stein=git_stein, squashedOutput=outputName, clusterNum=num,
             compareResult=CompareResult,RMSupportedREF=RMSupportedREF)

        time_end = timeRecord()
        t = time_end - time_start
        tResult = outputTime(t)
        print(tResult)
        with open(outputName+data["titan"]["time"], "w") as f:
            f.writelines(tResult)

if __name__ =="__main__":
    args=sys.argv
    repoPath=args[1]
    output=args[2]
    clusterNum = [2, 5]
    runServer(repoPath,output,clusterNum)