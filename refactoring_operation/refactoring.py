from line_trace import BlameRes
from line_trace import trace2
import pathlib
from repository import Repository


class Refactoring:
    def __init__(self, properties: dict):
        """
        Refactoring class
        :param properties:
        """
        self.properties = properties
        self.type = properties["type"]
        self.left = RefLocation(properties.get("leftSideLocations")[0])
        self.right = RefLocation(properties.get("rightSideLocations")[0])
        try:
            self.refactored_location = RefactoredLocation(properties.get("leftSideLocations")[0]["startLine"],
                                                          properties.get("leftSideLocations")[0]["endLine"],
                                                          properties.get("leftSideLocations")[0]["filePath"],
                                                          properties.get("leftSideLocations")[0]["codeElement"])
        except IndexError("Refactoring does not have leftSideLocations property"):
            self.refactored_location = None
        self.refactored_source_location = {}

        self.traced_location = {}

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.__key() == other.__key():
                return True
            else:
                return False
        else:
            return NotImplemented

    def __key(self):
        return self.type, str(self.left), str(self.right), str(self.refactored_location)

    def __str__(self):
        return f"{self.type} {self.left.__str__()} {self.right.__str__()}  {self.refactored_location.__str__()}"

    def trace_source_location(self, commit_sha1: str, repo: Repository,
                              ignore_commits: "list[Commit]") -> 'Refactoring':
        """
        Use git blame to trace the refactored code for where the code is firstly introduced
        trace with only the startLine of the refactored code
        :param ignore_commits: commits needed to be ignored during tracing
        :param commit_sha1:
        :param repo:
        :return:
        """
        self.refactored_source_location = trace2(
            (self.refactored_location.startLine, self.refactored_location.startLine),
            commit_sha1,
            str(self.refactored_location.file_path),
            repo,
            ignore_commits
        )
        return self

    def set_source_location(self, properties: dict) -> 'Refactoring':
        """
        Load source location from file
        :return:
        """
        source_locations = properties.get("sourceLocations", None)
        self.refactored_source_location = []
        if source_locations:
            for each in source_locations:
                self.refactored_source_location.append(BlameRes(each["sha1"], each["oline"], each["file_name"]))
        return self

    def load_traced_location(self):
        """
        load the traced result
        :return:
        """
        traced = self.properties.get("traced", None)
        if not traced:
            return
        for num_of_ignored_commit in traced:
            info = traced[num_of_ignored_commit]
            self.traced_location[num_of_ignored_commit] = BlameRes(info["sha1"], info["oline"], info["file_name"])
        return self

    def get_dict_format(self):
        return {
            "type": self.type,
            "leftSideLocations": [{"startLine": self.refactored_location.startLine,
                                   "endLine": self.refactored_location.endLine,
                                   "filePath": self.left.filePath,
                                   "codeElement": self.left.codeElement}],
            "rightSideLocations": [{"filePath": self.right.filePath,
                                    "codeElement": self.right.codeElement}],
            "sourceLocations": [each.__dict__ for each in self.refactored_source_location]}

    def get_key(self):
        return self.__key()

    def to_traced_dict(self):
        return {
            "type": self.type,
            "leftSideLocations": [{"startLine": self.refactored_location.startLine,
                                   "endLine": self.refactored_location.endLine,
                                   "filePath": self.left.filePath,
                                   "codeElement": self.left.codeElement}],
            "rightSideLocations": [{"filePath": self.right.filePath,
                                    "codeElement": self.right.codeElement}],
            "traced": self.traced_location
        }


class RefactoredLocation:
    def __init__(self, start_line, end_line, file_path, codeElement):
        self.startLine = start_line  # Start line number of the refactored code
        self.endLine = end_line  # End line number of the refactored code
        self.file_path = file_path  # File path of the refactored code
        self.codeElement = codeElement

    def __str__(self):
        return f"{self.file_path} {self.startLine}:{self.endLine}"


class RefLocation:
    def __init__(self, prop: dict):
        self.filePath = prop.get("filePath", "")
        self.codeElement = prop.get("codeElement", "")

    def __str__(self):
        codeElement = self.codeElement
        if not codeElement:  # codeElement can be null for some of the Refactorings (Inline Variable: rightSideLocations, Extract Variable: leftSideLocations)
            codeElement = ""
        return self.filePath + "@" + codeElement

    def __key(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.__key() == other.__key():
                return True
            else:
                return False
        else:
            return NotImplemented


class RefRM(Refactoring):
    pass


class RefRd(Refactoring):
    pass
