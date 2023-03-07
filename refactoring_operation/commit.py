import json
from refactoring_operation.refactoring import Refactoring, RefRM
import pathlib
import subprocess
from refactoring_operation.supported_ref_type import NotSupportedRefType


class Commit:
    """
    Commit load from json file, json file can be output of refactoring miners (RefactoringMiner, RefDiff)
    """

    def __init__(self, file_p):
        with open(file_p) as f:
            data = json.load(f)
        self.sha1 = pathlib.Path(file_p).name.split(".")[0]
        self.commit_raw = data.get("commits", None)
        self.refs = []
        if self.commit_raw:
            self.refs = self._extrac_refs()

    def get_refs(self):
        return self.refs

    def _extrac_refs(self):
        refs_raw = self.commit_raw[0].get("refactorings", None)
        refs = []
        if refs_raw:
            for r in refs_raw:
                if not r["type"] in [not_supported.value for not_supported in NotSupportedRefType]:
                    refs.append(Refactoring(r))
        return refs

    def dump_refs(self, directory: str):
        """
        dump
        :param directory:
        :return:
        """
        directory = pathlib.Path(directory)
        if not directory.exists():
            directory.mkdir()
        file = directory.joinpath(self.sha1 + ".json")
        if len(self.refs):  # exclude commits with no refs
            with open(file, "w") as f:
                json.dump([ref.get_dict_format() for ref in self.refs], f)

    def trace_refs_source_locations(self, parent_commit_sha1: str, repo: 'Repository') -> 'Commit':
        """
        trace refs source locations
        :return:
        """
        for ref in self.refs:
            ref.trace_source_location(parent_commit_sha1, repo)
        return self


class RMCommit(Commit):
    def __init__(self, p):
        '''
        initialize the commit with a RefactoringMiner json output
        :param p: path for the RefactoringMiner json output
        '''
        super().__init__(p)
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


def exclude_ref_type():
    pass