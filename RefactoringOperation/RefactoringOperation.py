class RefactoringOperation:
    def __init__(self,refactoringOperation:str,belongedCommit:str):
        self.type = refactoringOperation["type"]
        self.description = refactoringOperation["description"]
        self.leftSideStartColumn = refactoringOperation["leftSideLocations"][0]["startColumn"]
        self.leftSideEndColumn = refactoringOperation["leftSideLocations"][0]["endColumn"]
        self.leftFilePath = refactoringOperation["leftSideLocations"][0]["filePath"]
        self.rightFilePath = refactoringOperation["rightSideLocations"][0]["filePath"]
        self.belongedCommit = belongedCommit

    def __key(self):
        return self.type, self.description, self.leftSideStartColumn, self.leftSideEndColumn, self.leftFilePath, self.rightFilePath

    def __eq__(self, other):
        if isinstance(other,self.__class__):
            if self.__key() == other.__key():
                return True
            else:
                return False
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return str(self.__key())