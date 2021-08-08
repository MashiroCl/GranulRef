import os

class RefactoringMiner:
    def __init__(self,path):
        self.RMPath=path

    def detect(self,repository,output,commitID:str):
        print("commitID is ",commitID)
        command = self.RMPath + ' -c ' + repository + ' ' + commitID + ' -json ' + output + "/" +commitID+".json"

        os.system(command)
        print(command)
        return output + "/" + commitID + ".json"