import json
from refactoring_operation.refactoring import RefRM

class Commit():
    def __init__(self, p):
        pass

    def get_refs(self):
        pass

class RMCommit(Commit):
    def __init__(self, p):
        '''
        initialize the commit with a RefactoringMiner json output
        :param p: path for the RefactoringMiner json output
        '''
        self.refs = None
        with open(p) as f:
            data = json.load(f)
        commit_raw = data.get("commits", None)

        if commit_raw:
            self.sha1 = commit_raw[0].get("sha1", None)
            refs = commit_raw[0].get("refactorings", None)
            if refs:
                self.refs = [RefRM(r) for r in refs]

    def get_refs(self):
        return self.refs