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
        print("Folder " + folder + " already exists, Directory recreated")
        os.system("rm -rf "+folder)
        os.mkdir(path)
    return path


class MyRepository:
    def __init__(self,path):
        self.repoPath=path
        self.outputPath="./output"
        self.comparePath="./compare"

    def createWorkSpace(self):
        create_folder(self.outputPath)
        create_folder(self.comparePath)

    #copy commits into cc_cluster_info.txt at repository
    def cc_cluster_info(self, commits):
        cc_cluster_info = self.repoPath + "/cc_cluster_info.txt"
        f1 = open(cc_cluster_info, "w")
        f1.write("#!/usr/bin/vi\n")
        for each in commits:
            f1.write(each.commitID)
        f1.close()

    #copy auto_seq_editor to repository
    def copy_auto_seq_editor(self):
        auto_seq_editor = self.repoPath + '/auto-seq-editor.rb'
        f2 = open(auto_seq_editor, 'w')
        f3 = open('./auto-seq-editor.rb')
        lines = f3.readlines()
        for each in lines:
            f2.write(each)
        f2.close()
        f3.close()
        os.system("chmod 777 " + self.repoPath + "/auto-seq-editor.rb")

    #Combine multiple RM results which are in output files into one file
    def combine(self,combinedJsonFile)->str:
        result = []
        for f in glob.glob(self.outputPath+ "/" + "*.json"):
            with open(f, "r") as infile:
                result.append(json.load(infile))
        file=self.comparePath + combinedJsonFile
        with open(file, "w") as outfile:
            json.dump(result, outfile)
        return file

    # squash the commits specified in the cc_cluster_info.txt
    def squashCommits(self,parentCommit:Commit):
        print("start squash")
        cc_cluster_info = self.repoPath + '/cc_cluster_info.txt'
        auto_seq_editor = self.repoPath + '/auto-seq-editor.rb'
        git_rebase = 'git rebase -i ' + parentCommit.commitID
        f1 = open(self.repoPath + "/squash.sh", 'w')
        command = "env " + "CC_CLUSTER_INFO=" + cc_cluster_info + ' ' + 'GIT_SEQUENCE_EDITOR=' + auto_seq_editor + ' ' + git_rebase
        f1.write('cd ' + self.repoPath + '\n' + command)
        f1.close()
        os.system('echo :wq| sh ' + self.repoPath + "/squash.sh")
