titan_dataset_dir = "/home/salab/chenlei/CGR/dataset/"
titan_output_dir = "/home/salab/chenlei/CGR/experiment/output/"
local_dataset_dir = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/"
local_output_dir = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"


def remove_comment(dataset_dir, output_dir, repo, mount=True):
    if mount:
        command = f"nohup python3 remove_comment.py -s {dataset_dir}{repo} -t {output_dir}{repo}_cr >runlog/{repo}_cr.log 2>&1 &"
    else:
        command = f"python3 remove_comment.py -s {dataset_dir}{repo} -t {output_dir}{repo}_cr >runlog/{repo}_cr.log"
    print(command)


def detect_refactoring(dataset_dir, output_dir, repo, mount=True):
    if mount:
        for i in range(1, 6):
            print(
                f"nohup python3 command.py -r {dataset_dir}{repo}_cr -c {i} -o {output_dir} >runlog/{repo}_cr_ref_{i}.log 2>&1 &")
    else:
        for i in range(1, 6):
            print(f"python3 command.py -r {dataset_dir}{repo}_cr -c {i} -o {output_dir} >runlog/{repo}_cr_ref_{i}.log")


def trace_refactoring(dataset_dir, ref_dir, repo, mount=True):
    if mount:
        print(
            f"nohup python3 trace.py -f {ref_dir}{repo}_cr -r {dataset_dir}{repo}_cr/.git >runlog/{repo}_trace.log 2>&1 &")
    else:
        print(f"python3 trace.py -f {ref_dir}{repo}_cr -r {dataset_dir}{repo}_cr/.git >runlog/{repo}_trace.log")


def attach_descriptions(ref_dir, repo, mount=True):
    if mount:
        print(
            f"nohup python3 attach_descriptions.py -r {ref_dir}{repo}_cr >runlog/{repo}_attach.log 2>&1 &")
    else:
        print(f"python3 attach_descriptions.py -r {ref_dir}{repo}_cr >runlog/{repo}_attach.log")

def collect_cgr_fgr_repo(dataset_dir, ref_dir, repo, mount=True):
    if mount:
        print(
            f"nohup python3 coarse_fine_ref_extractor.py -p {ref_dir}{repo}_cr -c {dataset_dir}{repo}_cr -r {repo} >runlog/{repo}_collect2csv.log 2>&1 &")

    else:
        print(f"python3 coarse_fine_ref_extractor.py -p {ref_dir}{repo}_cr -c {dataset_dir}{repo}_cr -r {repo} >runlog/{repo}_collect2csv.log")



if __name__ == "__main__":

    temp = """javapoet
                mbassador
                seyren
                jeromq
                jfinal
                retrolambda
                helios
                android-async-http
                baasbox
                RoboBinding
                sshj
                zuul
                giraph
                truth
                spring-data-rest
                blueflood
                goclipse
                rest-assured
                cascading
                HikariCP
                hydra
                PocketHub
                rest.li
                morphia
                xabber-android
                redisson
                Activiti
                processing
                checkstyle
                libgdx
                cgeo
                JGroups
                """

    repos = temp.split()

    # 5/18 evaluate time consumption for reviewer's comment
    repos = ["mbassador"]
    for repo in repos:
        # remove_comment(dataset_dir=titan_dataset_dir, output_dir=titan_dataset_dir, repo=repo)
        detect_refactoring(dataset_dir=local_dataset_dir, output_dir=local_output_dir, repo=repo, mount=True)
        # detect_refactoring(dataset_dir=titan_dataset_dir, output_dir=titan_output_dir, repo=repo, mount=True)
        # trace_refactoring(dataset_dir=local_dataset_dir, ref_dir=local_output_dir, repo=repo, mount=True)
        # trace_refactoring(dataset_dir=titan_dataset_dir, ref_dir=titan_output_dir, repo=repo, mount=True)

        # attach_descriptions(ref_dir=titan_output_dir, repo=repo, mount=True)

        # collect_cgr_fgr_repo(titan_dataset_dir, titan_output_dir, repo)
