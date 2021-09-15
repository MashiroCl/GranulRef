commits=956
temp="1h 8min 19s	1h 7min 44s	 1h 0min 27s"
tempList=[]
for each in temp.split("s"):\
    tempList.append(each.strip())
for time in tempList[0:3]:
    hour = int(time.split("h")[0])
    min = int(time.split("min")[0].split("h")[1])
    s = int(time.split("min")[1].split("s")[0])
    miao=hour*3600+min*60+s
    print(commits/miao)

