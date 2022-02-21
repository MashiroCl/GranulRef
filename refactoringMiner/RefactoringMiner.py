import os

class RefactoringMiner:
    def __init__(self,path):
        self.RMPath=path

    def detect(self,repository,output,commitID:str):

        command = self.RMPath + ' -c ' + repository + ' ' + commitID + ' -json ' + output + "/" +commitID+".json"
        os.system(command)
        # print(command)
        return output + "/" + commitID + ".json"


if __name__ =="__main__":
    RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
    rm = RefactoringMiner(RMPath)
    repository = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/retrolambda"
    output = "/Users/leichen/Desktop"
    commitID = "bc99e75c2fa4b56325910e445283d1b24cb2618d"
    rm.detect(repository,output,commitID)