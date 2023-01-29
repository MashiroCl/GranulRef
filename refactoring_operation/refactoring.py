from typing import List
from dataclasses import dataclass
from line_trace import BlameRes

class Refactoring():
    def __init__(self):
        pass

    def __hash__(self):
        pass

@dataclass
class RefactoredLocation:
    startLine:str  # Start line number of the refactored code
    endLine:str  # End line number of the refactored code
    file_path:str  # File path of the refactored code

class RefRM(Refactoring):
    def __init__(self, prop):
        '''
        RefactoringMiner detected refactoring
        :param prop: a dict contains
            refactoring type
            leftSideLocations: [(filePath, codeElement),(filePath, codeElement)]
            rightSideLocations: [(filePath, codeElement),(filePath, codeElement)]
            description
        '''
        super().__init__()
        self.type = prop["type"]
        self.description = prop["description"]
        self.left = self._load_location(prop, "leftSideLocations")
        self.right = self._load_location(prop, "rightSideLocations")
        self.refactored_location = self._load_refactored_location(prop)  # in leftSideLocation (startLine, endLine) & the file_path
        self.oline = None  # original line number: where the refactored code is firstly introduced

    def _load_location(self, prop, location_name):
        res = []
        if len(prop[location_name]) > 0:
            ref_location = prop[location_name][0]
            res.append((ref_location["filePath"], ref_location["codeElement"]))
        return res

    def _load_refactored_location(self, prop):
        # load leftSideLocation startLine, endLine and the file path
        return RefactoredLocation(prop["leftSideLocations"][0]["startLine"],
                                  prop["leftSideLocations"][0]["endLine"],
                                  prop["leftSideLocations"][0]["filePath"])

    def _location2str(self, location):
        res = ""
        for each in location:
            filePath = each[0]
            # for ref Extract Mehtod, its codeElement of the 2nd leftSideLocation is null, set it to str null to
            # avoid that different refs may have the same hash key
            if not each[1]:
                codeElement = "null"
            else:
                codeElement = each[1]
            res += "#" + filePath + "@" + codeElement
        return res

    def __key(self):
        def parse_oline(oline: List[BlameRes]) -> str:
            res = ""
            for each in oline:
                res += "#"
                res += "@".join([each.sha1, each.oline, each.file_name])
            return res
        return self.type, self._location2str(self.left), self._location2str(self.right), parse_oline(self.oline)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.__key() == other.__key():
                return True
            else:
                return False
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return f"type:{self.type}\tleft:{self.left}\tright:{self.right}\tdescription:{self.description}"

    def set_oline(self, oline: List[BlameRes]):
        self.oline = oline
