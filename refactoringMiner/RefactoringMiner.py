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
    RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"
    rm = RefactoringMiner(RMPath)
    repository = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/RTE/testsquash"
    output = "/Users/leichen/Desktop/"
    commitID = "fd41b95d97e53b8a4725ba0dc72eababedb0f373"
    rm.detect(repository,output,commitID)