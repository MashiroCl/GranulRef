from line_trace import BlameRes, trace
import pathlib
from repository import Repository


class Refactoring:
    def __init__(self, properties: dict):
        """
        Refactoring class
        :param properties:
        """
        self.type = properties["type"]
        self.left = RefLocation(properties.get("leftSideLocations")[0])
        self.right = RefLocation(properties.get("rightSideLocations")[0])
        try:
            self.refactored_location = RefactoredLocation(properties.get("leftSideLocations")[0]["startLine"],
                                                          properties.get("leftSideLocations")[0]["endLine"],
                                                          properties.get("leftSideLocations")[0]["filePath"])
        except IndexError("Refactoring does not have leftSideLocations property"):
            self.refactored_location = None
        self.refactored_source_location = None

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
        def parse_source_location(source_locations: list[BlameRes]) -> str:
            res = ""
            for each in source_locations:
                res += "#"
                res += "@".join([each.sha1, each.oline, each.file_name])
            return res

        # location refactored code (startLine, endLine) cannot be used
        # as the hash key because it will be affected by commit squash
        if self.refactored_source_location:
            return self.type, self.left.__str__(), self.right.__str__(), parse_source_location(
                self.refactored_source_location)
        else:
            return self.type, self.left.__str__(), self.right.__str__()

    def __str__(self):
        return self.type + self.left.__str__() + self.right.__str__() + self.refactored_location.__str__()

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
        self.refactored_source_location = trace(
            (self.refactored_location.startLine, self.refactored_location.startLine),
            commit_sha1,
            pathlib.Path(repo.repoPath).joinpath(
                self.refactored_location.file_path).__str__(),
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


class RefactoredLocation:
    def __init__(self, start_line, end_line, file_path):
        self.startLine = start_line  # Start line number of the refactored code
        self.endLine = end_line  # End line number of the refactored code
        self.file_path = file_path  # File path of the refactored code

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