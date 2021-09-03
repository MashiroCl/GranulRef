import os
import json
import glob
from Commit import Commit

#create a folder to save information under current script path
def create_folder(folder):
    # folder= sys.argv[0]
    path=folder
    try:
        os.mkdir(path)
    except FileExistsError:
        # print("Folder " + folder + " already exists, Directory recreated")
        os.system("rm -rf "+folder)
        os.mkdir(path)
    return path


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

    #copy auto_seq_editor to repository
    def copy_auto_seq_editor(self):
        auto_seq_editor = self.repoPath + '/auto-seq-editor.py'
        f2 = open(auto_seq_editor, 'w')
        f3 = open('./auto-seq-editor.py')
        lines = f3.readlines()
        for each in lines:
            f2.write(each)
        f2.close()
        f3.close()
        os.system("chmod 777 " + self.repoPath + "/auto-seq-editor.py")

    #Combine multiple RM results which are in output files into one file
    def combine(self,combinedJsonFile)->str:
        result = []
        for f in glob.glob(self.RMoutputPath+ "/" + "*.json"):
            with open(f, "r") as infile:
                result.append(json.load(infile))
        path=self.comparePath + combinedJsonFile
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
        print('start squash')
       # command="java -jar "+git_stein+" Clusterer "+"--recipe="+recipe+" -v -o "+output+" "+repository+">"+"./stein.log"
        command="java -jar "+git_stein+" Clusterer "+"--recipe="+recipe+" -v -o "+output+" "+repository+">"+"./stein.log"
        # print("command is ", command)
        os.system(command)
