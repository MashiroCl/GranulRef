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

if __name__ == "__main__":
    pass