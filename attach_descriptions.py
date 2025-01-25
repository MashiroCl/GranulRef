import argparse
import pathlib
import json


def overwrite_add_description(f_d: pathlib.Path, f_no_d: pathlib.Path):
    def build_key(ref):
        key = {"type": ref["type"]}

        try:
            leftSideLocation = ref["leftSideLocations"][0]
            key["leftSideLocations"] = {}
            key["leftSideLocations"]["startLine"] = leftSideLocation["startLine"]
            key["leftSideLocations"]["endLine"] = leftSideLocation["endLine"]
            key["leftSideLocations"]["filePath"] = leftSideLocation["filePath"]
            key["leftSideLocations"]["codeElement"] = leftSideLocation["codeElement"]

            rightSideLocation = ref["rightSideLocations"][0]
            key["rightSideLocations"] = {}
            key["rightSideLocations"]["filePath"] = rightSideLocation["filePath"]
            key["rightSideLocations"]["codeElement"] = rightSideLocation["codeElement"]
        except IndexError:
            key = ""

        return str(key)

    with open(f_d) as f:
        ref_json_des = json.load(f)
    ref_descriptions = {}
    for ref in ref_json_des["commits"][0]["refactorings"]:
        key = build_key(ref)
        if len(key):
            ref_descriptions[str(key)] = ref["description"]

    with open(f_no_d, "r") as f:
        ref_json_no_des = json.load(f)
        for ref in ref_json_no_des["refactorings"]:
            key = build_key(ref)
            if len(key):
                ref["description"] = ref_descriptions.get(key, "")
    with open(f_no_d, "w") as f:
        json.dump(ref_json_no_des, f)


def attach_descriptions(repo_path):
    for i in range(1, 2):
        traced_directory = pathlib.Path(repo_path).joinpath("o" + str(i))
        for commitIDjson in traced_directory.iterdir():
            origin_path = (
                pathlib.Path(repo_path)
                .joinpath(str(i))
                .joinpath("refs")
                .joinpath(commitIDjson.name)
            )
            overwrite_add_description(f_d=origin_path, f_no_d=commitIDjson)


if __name__ == "__main__":
    # repo_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador_cr"
    # attach_descriptions(repo_path)

    parser = argparse.ArgumentParser(
        description="Attach refactoring descriptions to the traced refactoring files"
    )
    parser.add_argument("-r", help="repository path")
    args = parser.parse_args()
    attach_descriptions(args.r)
