import json
import pathlib
from typing import Union
from refactoring_operation.refactoring import Refactoring


def load_dictref(file_p: Union[str, pathlib.Path]) -> list[Refactoring]:
    refs = []
    if not pathlib.Path(file_p).exists():
        return refs
    with open(file_p) as f:
        data = json.load(f)
    if not isinstance(data, list):  # no refactoring detected in the commit
        return refs
    for ref_d in data:
        refs.append(Refactoring(ref_d).set_source_location(ref_d))
    return refs


def load_traced_refs(file_p: str) -> list[Refactoring]:
    refs = []
    if not pathlib.Path(file_p).exists():
        return refs
    with open(file_p) as f:
        data = json.load(f)
    for ref_d in data.get("refactorings", []):
        refs.append(Refactoring(ref_d).load_traced_location())
    return refs


def load_retrace_dictref(file_p, ignored_commit_count) -> list[Refactoring]:
    refs = []
    if not pathlib.Path(file_p).exists():
        return refs
    with open(file_p) as f:
        data = json.loads("[" + f.read() + "]")[0][str(ignored_commit_count)]["refs"]
    if not isinstance(data, list):  # no refactoring detected in the commit
        return refs
    for ref_d in data:
        refs.append(Refactoring(ref_d).set_source_location(ref_d))
    return refs


def load_dictref_no_source(file_p: Union[str, pathlib.Path]) -> list[Refactoring]:
    refs = []
    if not pathlib.Path(file_p).exists():
        return refs
    with open(file_p) as f:
        data = json.load(f)["commits"]
    if not len(data):
        return refs
    for ref_d in data[0]["refactorings"]:
        if (
            ref_d["type"] == "Move Source Folder"
        ):  # Move Source Folder has no leftSideLocations and rightSideLocations
            continue
        refs.append(Refactoring(ref_d))
    return refs


@DeprecationWarning
def get_commit_refdict(
    squash_log_p: str, commits: Union[str, list[str]], coarse_grained_commit: str = ""
) -> list[list[Refactoring]]:
    refs_d = pathlib.Path(squash_log_p).parent.parent
    squash_num = pathlib.Path(squash_log_p).name.split(".txt")[0].split("log")[1]
    refs = []
    if isinstance(commits, list):  # normal grained commits
        if len(coarse_grained_commit) == 0:
            raise Exception(
                "Coarse grained commit miss, directory for normal grained commits not set"
            )
        fine_grained_path = refs_d.joinpath(f"o{squash_num}").joinpath(
            coarse_grained_commit
        )
        for commit in commits:
            refs.append(load_dictref(fine_grained_path.joinpath(commit + ".json")))
    else:  # coarse grained commits
        coarse_grained_path = refs_d.joinpath(f"o{squash_num}")
        refs.append(load_dictref(coarse_grained_path.joinpath(commits + ".json")))
    return refs


def load_normal_grained_refs(file_p: str) -> list[Refactoring]:
    refs = []
    if not pathlib.Path(file_p).exists():
        return refs
    with open(file_p) as f:
        data = json.load(f)
    for ref_d in data.get("refactorings", []):
        refs.append(Refactoring(ref_d))
    return refs


def load_coarse_grained_refs(
    ref_folder: pathlib.Path, squash_num: int, commit: str
) -> list[Refactoring]:
    coarse_grained_path = ref_folder.joinpath(f"o{squash_num}")
    return load_dictref(coarse_grained_path.joinpath(commit + ".json"))


def get_retraced_commit_refdict2(
    squash_log_p: str, coarse_grained_commit, ignored_commit_count, sub_length
) -> list[list[Refactoring]]:
    refs_d = pathlib.Path(squash_log_p).parent.parent.joinpath("retrace")
    if not refs_d.exists():
        raise Exception(f"Retracing not conduct for {refs_d}")
    squash_num = pathlib.Path(squash_log_p).name.split(".txt")[0].split("log")[1]
    refs = []
    coarse_grained_path = refs_d.joinpath(
        str(sub_length), coarse_grained_commit + ".json"
    )
    # print("coarse_grained_path", coarse_grained_path)
    if ignored_commit_count == 0:
        # no retrace required
        # 11/21 change the not retrace case
        # refs_p = pathlib.Path(squash_log_p).parent.parent.joinpath("o" + str(int(squash_num) - 1)).joinpath(
        #     coarse_grained_commit + ".json")
        refs_p = (
            pathlib.Path(squash_log_p)
            .parent.parent.joinpath("o" + str(sub_length))
            .joinpath(coarse_grained_commit + ".json")
        )
        refs.append(load_dictref(refs_p))
    elif coarse_grained_path.exists():
        refs.append(load_retrace_dictref(coarse_grained_path, ignored_commit_count))
    return refs


def load_retraced_commit_refdict(
    ref_folder: pathlib.Path, coarse_grained_commit, ignored_commit_count, sub_length
) -> list[list[Refactoring]]:
    refs_d = ref_folder.joinpath("retrace")
    if not refs_d.exists():
        raise Exception(f"Retracing not conduct for {refs_d}")
    refs = []
    coarse_grained_path = refs_d.joinpath(
        str(sub_length), coarse_grained_commit + ".json"
    )
    if ignored_commit_count == 0:
        refs_p = ref_folder.joinpath("o" + str(sub_length)).joinpath(
            coarse_grained_commit + ".json"
        )
        refs.append(load_dictref(refs_p))
    elif coarse_grained_path.exists():
        refs.append(load_retrace_dictref(coarse_grained_path, ignored_commit_count))
    return refs


def extract_coarse_grained_refs(
    coarse_grained_refs: list[list[Refactoring]],
    normal_grained_refs: list[list[Refactoring]],
) -> list[Refactoring]:
    return list(
        set(coarse_grained_refs[0])
        - set([ref for each in normal_grained_refs for ref in each])
    )


def extract_regular_refs_by_squashlog(squash_log_p: str) -> list[Refactoring]:
    squash_log_p = pathlib.Path(squash_log_p)
    refs_d = pathlib.Path(squash_log_p).parent.parent
    if not squash_log_p.name == "log1.txt":
        raise RuntimeError(
            f"squash log is {squash_log_p}, use log1.txt as the squash log"
        )

    fine_grained_path = refs_d.joinpath("1", "refs")
    refs = []
    for path in fine_grained_path.iterdir():
        refs += load_dictref_no_source(path)
    return refs


def extract_fine_grained_refs(
    coarse_grained_refs: list[list[Refactoring]],
    normal_grained_refs: list[list[Refactoring]],
) -> list[Refactoring]:
    return list(
        set([ref for each in normal_grained_refs for ref in each])
        - set(coarse_grained_refs[0])
    )


def extract_fine_grained_refs_through_type(
    coarse_grained_refs: list[list[Refactoring]],
    normal_grained_refs: list[list[Refactoring]],
) -> list[Refactoring]:
    """
    Obtain Fine Grained Refs by using Normal Grained Refs to substract Coarse Grained Refs
    :param coarse_grained_refs: list[list[squashed coarse grained refs]]
    :param normal_grained_refs: list[list[non-squashed normal grained refs],list[non-squashed normal grained refs]],
    each list[non-squashed normal grained refs] is squashed to the corresponding index coarse grained refs in coarse_grained_refs
    :return: list of Fine Grained Refs
    """
    CGRtypes = set([ref.type for ref in coarse_grained_refs[0]])
    NGRtypes = set([ref.type for each in normal_grained_refs for ref in each])
    return list(NGRtypes - CGRtypes)


def extract_coarse_grained_refs_thorough_types(
    coarse_grained_refs: list[list[Refactoring]],
    normal_grained_refs: list[list[Refactoring]],
) -> list[Refactoring]:
    """
    ICPC 2022
    if one type of refactoring is detected from only CGC but not NGCs, then we say that refactoring is a CGR
    :return:
    """
    NGRtypes = set([ref.type for each in normal_grained_refs for ref in each])
    CGRs = []
    for each in coarse_grained_refs[0]:
        if each.type not in NGRtypes:
            CGRs.append(each)
    return CGRs


def match_oline_as_supportive(
    coarse_grained_ref: Refactoring,
    normal_grained_ref: Refactoring,
) -> bool:
    """
    :param normal_grained_commit_sha1s:
    :param coarse_grained_ref: squashed coarse-grained ref, which is squashed by normal_grained_refs
    :param normal_grained_ref: one non-squashed normal-grained-ref
    :return: it is matched or not

    match mechanism for determine whether a refactoring detected from coarse-grained commit is the same as the
    normal-grained ref (match if yes)

    mechanism:
        2023.10.23 add the lossen the matching criteria, because if the trace of a coarse-grained commit is the commit
        in front

        1. strictly compare using the trace locaiton (oline)
        ref detected in coarse-grained commit Co: r'
        normal-grained commit {C1, C2}, which squashed into Co.
        refs detected in {C1, C2}: R
        r ∈ R
          r==r'<=> r.type==r'type ^ r.oline==r'.oline

        2. lossen the
    """
    # print("coarse grained ref type", coarse_grained_ref.type)
    # print("coarse grained ref left", coarse_grained_ref.left)
    # print("coarse grained ref right", coarse_grained_ref.right)
    #
    # print("normal grained ref type", normal_grained_ref.type)
    # print("normal grained ref left", normal_grained_ref.left)
    # print("normal grained ref right", normal_grained_ref.right)

    if (
        coarse_grained_ref.type == normal_grained_ref.type
        and coarse_grained_ref.refactored_source_location
        == normal_grained_ref.refactored_source_location
    ) or (
        coarse_grained_ref.type == normal_grained_ref.type
        and str(coarse_grained_ref.left) == str(normal_grained_ref.left)
        and str(coarse_grained_ref.right) == str(normal_grained_ref.right)
    ):
        return True
    return False


def match_with_traced_location(
    refA: Refactoring,
    num_of_ignored_commit_A: int,
    refB: Refactoring,
    num_of_ignored_commit_B: int,
) -> bool:
    """
    Checks if the two refactoring matches each other by comparing the 1) refactoring type, 2) refactoring target, 3) traced location
    :param num_of_ignored_commit_B:
    :param num_of_ignored_commit_A:
    :param refA:
    :param refB:
    :return:
    """
    # Since the order of elements in the Merge Package's leftSideLocation may change due to granularity level change,
    # the traced locations of the 1st element's leftSideLocation cannot be used anymore
    # We use the descriptions to compare for Merge Package
    if (
        refA.type == refB.type == "Merge Package"
        and refA.description == refB.description
    ):
        return True

    return (
        refA.type == refB.type
        and refA.refactored_location.codeElement == refB.refactored_location.codeElement
        and refA.traced_location[str(num_of_ignored_commit_A)]
        == refB.traced_location[str(num_of_ignored_commit_B)]
    )


def extract_coarse_grained_refs_oline_as_supportive(
    coarse_grained_refs: list[list[Refactoring]],
    normal_grained_refs: list[list[Refactoring]],
) -> list[Refactoring]:
    """
    Extract coarse grained refs through match mechanism
    :param coarse_grained_refs:
    :param normal_grained_refs:
    :return:
    """
    res = []
    CGR_candidates = coarse_grained_refs[0]
    NGRs = [ref for each in normal_grained_refs for ref in each]
    for CGR_candidate in CGR_candidates:
        if not any([match_oline_as_supportive(CGR_candidate, NGR) for NGR in NGRs]):
            # for each in NGRs:
            #     if str(CGR_candidate)==str(each) and str(each) == "Move Methodhelios-crtauth/src/test/java/com/spotify/helios/auth/crt/CrtAuthProviderTest.java@private hasStatus(sc int) : StatusCodeMatcherhelios-authentication/src/test/java/com/spotify/helios/auth/AuthInjectableProviderTest.java@private hasStatus(sc int) : StatusCodeMatcherhelios-crtauth/src/test/java/com/spotify/helios/auth/crt/CrtAuthProviderTest.java 105:107":
            #         print("found in both CGR and NGR")
            #         print("CGR", CGR_candidate.refactored_source_location)
            #         print("NGR", each.refactored_source_location)
            #         print(any([match_oline_as_supportive(CGR_candidate, NGR) for NGR in NGRs]))
            res.append(CGR_candidate)
    return res


class RefactoringSetOperation:
    """
    Simulate the operations between two set of refactorings, such as set subtraction
    """

    @staticmethod
    def subtract(a: set[Refactoring], b: set[Refactoring]):
        res = set()
        for aa in a:
            if not any([match_oline_as_supportive(aa, bb) for bb in b]):
                res.add(aa)

        return res
