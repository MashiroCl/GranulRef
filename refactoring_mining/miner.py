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
        return output + "/" + commitID + ".json"

