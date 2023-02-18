'''
Refactoring Miner class, implement detect method to detect refactoring operations in a commit
'''


import os


class RefactoringMiner:
    def __init__(self, path):
        self.RMPath = path

    def detect(self, repository, output, commitID: str):
        '''
        use RefactoringMiner to detect refactoring operations in a commit
        :param repository: repository path
        :param output: output directory
        :param commitID:
        :return: output json file path
        '''
        command = self.RMPath + ' -c ' + repository + ' ' + commitID + ' -json ' + output + "/" + commitID + ".json"
        os.system(command)



class RefDiff:
    def __init__(self, path):
        self.RDpath = path

    def detect(self, repository:str, output, commitID):
        repo_name = repository.split("/")[-1]
        repo_root = repository.split(repo_name)[0]
        command = f"java -jar {self.RDpath} -r {repo_root} -n {repo_name} -o {output} -c {commitID}"
        os.system(command)
