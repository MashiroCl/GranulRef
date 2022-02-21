import json
from RefactoringOperation.RefactoringOperation import RefactoringOperation
# from RefactoringOperation import RefactoringOperation

class RMcommit:
    def __init__(self,jsonPath):
        self.jsonPath = jsonPath
        self.commitID = ""
        self.refactorings=list()
        self._initFromRMjson()

    def _initFromRMjson(self):
        '''
        using result extracted from RefactoringMiner to initialize RefactoringOperation class
        :param jsonPath: file path for RefactoringMiner json result
        :return: sha1,type,description
        '''
        with open(self.jsonPath) as f:
            data = json.load(f)
        try:
            self.commitID = data["commits"][0]["sha1"]
            refactorings = data["commits"][0]["refactorings"]
            for each in refactorings:
                ro = RefactoringOperation(each,self.commitID)
                self.refactorings.append(ro)
        except KeyError:
            pass
        except IndexError:
            pass

if __name__ == "__main__":
    filePath1 = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/retrolambda/1/942e33cb76557e57c0bc062a66af7e6e78df2629.json"
    filePath2 = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/retrolambda/2/38ccdfa782185999c69edf7ba924dd60ed51d1ce.json"

    rMcommit = RMcommit(filePath1)
    rMcommit2 = RMcommit(filePath2)
    print(rMcommit.refactorings[0])
    print(rMcommit2.refactorings[2])
    # rMcommitSquashed = RMcommit(filePath2)
    # print(rMcommitSquashed.refactorings[1].description)
    # print(rMcommit.refactorings[1].description)
    # print(rMcommitSquashed.refactorings[1]==rMcommit.refactorings[1])
    # test = set()
    # for ro in rMcommit.refactorings:
    #     test.add(ro)
    # print(len(test))
    # for ro in rMcommit2.refactorings:
    #     test.add(ro)
    #
    # test2 = set()
    # for ro in rMcommitSquashed.refactorings:
    #     test2.add(ro)
    # test = test.union(test2)
    # print(len(test))