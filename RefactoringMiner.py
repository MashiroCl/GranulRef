import os
from Commit import Commit
class RefactoringMiner:
    def __init__(self,path):
        self.RMPath=path

    def detect(self,repository,output,commitID:str):
        command = self.RMPath + ' -c ' + repository + ' ' + commitID \
                  + ' -json ' + output + "/" + commitID + ".json"
        os.system(command)
