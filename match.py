import json
import pathlib
from typing import Union

from refactoring_operation.refactoring import Refactoring


def load_dictref(file_p: Union[str, pathlib.Path]) -> list[Refactoring]:
    refs = []
    with open(file_p) as f:
        data = json.load(f)
    for ref_d in data:
        refs.append(Refactoring(ref_d).set_source_location(ref_d))
    return refs
