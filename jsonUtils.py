import json
import os
from Commit import Commit

class JsonUtils:
    def __init__(self):
        self.repoPath=None
        self.jsonPath=None

    def setRepoPath(self,repoPath):
        self.repoPath=repoPath
    def setJsonPath(self,path):
        self.jsonPath=path

    'Get json format git commit info'
    def gitJson(self):
        if self.jsonPath==None:
            self.setJsonPath(self.repoPath+"/gitLog.json")
        prettyFormat="--pretty=format:\'{%n  \"commit\": \"%H\",%n \"tree\": \"%T\",%n \"parent\": \"%P\",%n \"commit_notes\": \"%N\",%n \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }%n},\'| sed \"$ s/,$//\""
        os.system('git -C ' + self.repoPath +' log '+prettyFormat +" >"+ self.jsonPath)

    'Read json file and return commit list'
    def jsonToCommit(self)->list:
        with open(self.jsonPath) as f:
            data = json.loads("[" + f.read() + "]")
        commits = []
        for each in data:
            commits.append(Commit(each))
        return commits

    'write recipe in json format'
    def writeRecipe(self,lists,path):
        recipe={}
        recipe["forcedClusters"]=[]
        for each in lists:
            recipe["forcedClusters"].append(each)
        with open(path,'w') as output:
           json.dump(recipe,output)
        print("recipe is ",recipe)
