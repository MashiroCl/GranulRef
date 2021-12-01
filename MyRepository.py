import os
import json
import glob


#create a folder to save information under current script path
def create_folder(folder):
    path=folder
    try:
        os.mkdir(path)
    except FileExistsError:
        os.system("rm -rf "+folder)
        os.mkdir(path)
    return path

def delete_foler(folder):
    try:
        os.system("rm -rf "+folder)
    except FileNotFoundError:
        print("File not found")


class MyRepository:
    def __init__(self,path):
        self.repoPath=path
        self.RMoutputPath="./RMoutput"
        self.RMoutputPathBS="./RMoutputBS"
        self.RMoutputPathAS="./RMoutputAS"
        self.comparePath="./compare"

        self.RMoutputPath=self.repoPath+"/RMoutput"
        self.comparePath = self.repoPath+"/compare"


    def setComparePath(self,s:str):
        self.comparePath=s
    def setRMoutputPath(self,s:str):
        self.RMoutputPath=s

    def createWorkSpace(self):
        create_folder(self.RMoutputPath)
        create_folder(self.comparePath)

    #copy commits into cc_cluster_info.txt at repository
    def cc_cluster_info(self, commits):
        cc_cluster_info = self.repoPath + "/cc_cluster_info.txt"
        f1 = open(cc_cluster_info, "w")
        f1.write("#!/usr/bin/vi\n")
        for each in commits:
            f1.write(each.commitID+"\n")
        f1.close()


    #Combine multiple RM results which are in output files into one file
    def combine(self,combinedJsonFileName)->str:
        result = []
        for f in glob.glob(self.RMoutputPath+ "/" + "*.json"):
            with open(f, "r") as infile:
                result.append(json.load(infile))
        path=self.comparePath + combinedJsonFileName
        with open(path, "w") as outfile:
            json.dump(result, outfile)
        return path

    def combinePart(self,combinedJsonFileName,beingSquashedFileName)->str:
        result = []
        for each in beingSquashedFileName:
            f = self.RMoutputPath+ "/" +each+ ".json"
            with open(f, "r") as infile:
                result.append(json.load(infile))
        path=self.comparePath + combinedJsonFileName
        with open(path, "w") as outfile:
            json.dump(result, outfile)
        return path

    def addRemote(self,path:str):
        command="(cd "+path+" && git remote add origin https://example.jp/dummy_url.git)"
        os.system(command)

    def gitGc(self,path:str):
        command="(cd "+path+" && git gc --aggressive --prune=now)"
        os.system(command)
    '2021/7/9 Discard this version Changed to shi5i git stein https://github.com/sh5i/git-stein'


    'sh5i git stein version https://github.com/sh5i/git-stein, squash according to recipe.json'
    def squashCommits(self,recipe,git_stein,output,repository):
        '''
        :param recipe: path for recipe.json
        :param git_stein: path for git-stein-all.jar
        :param output:  path for new .git output
        :param repository: path for being squashed repository
        :return:
        '''
        # print('start squash')
       # command="java -jar "+git_stein+" Clusterer "+"--recipe="+recipe+" -v -o "+output+" "+repository+">"+"./stein.log"
        command="java -jar "+git_stein+" Clusterer "+"--recipe="+recipe+" -v -o "+output+" "+repository+">"+"./stein.log"
        # print("command is ", command)
        os.system(command)
