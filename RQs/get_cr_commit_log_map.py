import subprocess
import json


def get_git_log(repository_path):
    # Change to the repository directory
    cwd = repository_path
    cmd = ['git', 'log', '--all', '--pretty=format:{"commit": "%H", "notes":"%N}']
    try:
        output = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error executing Git command: {e.output.decode('utf-8')}")
        return None


if __name__ == "__main__":
    # Specify the path to your Git repository
    repos = ["jfinal",
             "mbassador",
             "javapoet",
             "jeromq",
             "seyren",
             "retrolambda",
             "baasbox",
             "sshj",
             "xabber-android",
             "android-async-http",
             "giraph",
             "spring-data-rest",
             "blueflood",
             "HikariCP",
             "redisson",
             "goclipse",
             "morphia",
             "PocketHub",
             "hydra",
             "cascading",
             "helios",
             "RoboBinding",
             "truth",
             "rest.li",
             "rest-assured",
             "JGroups",
             "processing",
             "zuul"
             ]

    for repo in repos:
        repo = repo+"_cr"
        repository_path = '/home/salab/chenlei/CGR/dataset/'+repo
        git_log_json = get_git_log(repository_path)
        # skip the first commit which is a "git notes added" the last char is ,
        git_log_json = "{\"commits\":[" + git_log_json.replace("\n}", "\"},")[66:-1].replace("\n", "") + "]}"
        print(git_log_json)
        git_log = json.loads(git_log_json)
        d = dict()
        for each in git_log["commits"]:
            d[each["commit"]] = each["notes"]
        # Specify the path to the output file
        output_file = f'./{repo}.json'

        # Save the Git log to a text file
        with open(output_file, 'w') as file:
            json.dump(d, file)

        print(f"Git log saved to {output_file}.")
