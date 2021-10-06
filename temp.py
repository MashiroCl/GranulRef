def timeProcess(time):
    hour = int(time.split("h")[0])
    min = int(time.split("min")[0].split("h")[1])
    s = int(time.split("min")[1].split("s")[0])
    miao=hour*3600+min*60+s
    return miao

def calculateAverageSpeed():
    commits=8036
    temp=" 6h 39min 11s	21h 54min 33s	 31h 12min 52s	 39h 1min 12s"
    tempList=[]
    for each in temp.split("s"):\
        tempList.append(each.strip())
    for time in tempList[0:4]:
        hour = int(time.split("h")[0])
        min = int(time.split("min")[0].split("h")[1])
        s = int(time.split("min")[1].split("s")[0])
        miao=hour*3600+min*60+s
        print(commits/miao)

def calculateAverageSpeed2():
    commits=[7820.0,		7737.0,	 	7672.0]
    temp="21h 54min 33s	 31h 12min 52s	 39h 1min 12s"
    tempList=[]
    for each in temp.split("s"):
        tempList.append(each.strip())
    for i in range(0,3):
        print(commits[i],timeProcess(tempList[i]))
        print(commits[i]/timeProcess(tempList[i]))


if __name__ =="__main__":
    calculateAverageSpeed2()

