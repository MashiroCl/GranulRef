import unittest
from pathlib import Path
import shutil
import tempfile
from extract_refs import run, attach_source_locations
import subprocess


class TestProcess(unittest.TestCase):
    def test_process(self):
        repo = "refactoring-toy-example_cr"
        repo_path = f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/{repo}"

        output_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"
        output_dir = Path(output_path).joinpath(repo)
        if output_dir.exists() and output_dir.is_dir():
            shutil.rmtree(output_dir)

        command = [
            "nohup",
            "python3",
            "command.py",
            "-r",
            repo_path,
            "-c", "1",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)

        with open(f"run_log/{repo}1.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)


        command = [
            "nohup",
            "python3",
            "command.py",
            "-r",
            repo_path,
            "-c", "2",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}2.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)


        command = [
            "nohup",
            "python3",
            "command.py",
            "-r",
            repo_path,
            "-c", "3",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}3.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)


        command = [
            "nohup",
            "python3",
            "command.py",
            "-r", repo_path,
            "-c", "4",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}4.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        command = [
            "nohup",
            "python3",
            "command.py",
            "-r", repo_path,
            "-c", "5",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}5.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("2").joinpath("refs").glob("*.json")]
        assert len(jsons_refs) == 5
        jsons_refs = [each for each in dir_path.joinpath("3").joinpath("refs").glob("*.json")]
        assert len(jsons_refs) == 2

        # Trace
        command = [
            "nohup",
            "python3",
            "command.py",
            "-m",
            "trace",
            "-r", repo_path,
            "-d",
            f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/{repo}/",
            "--start",
            "2",
            "--end",
            "5"
        ]
        print("running command: ", command)
        with open(f"run_log/so_tr_{repo}.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("o2").rglob("*.json")]
        assert len(jsons_refs) == 10

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("o3").rglob("*.json")]
        assert len(jsons_refs) == 8

        # Retrace
        command = ["python3",
                   "retrace.py",
                   "-t",
                   "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/refactoring-toy-example_cr/",
                   "-r", repo_path,
        ]
        print("running command: ", command)
        with open(f"run_log/retrace_{repo}.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("retrace").rglob("*.json")]
        assert len(jsons_refs) == 5


    def test_process_mbassador(self):
        repo = "mbassador_cr"
        repo_path = f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/{repo}"

        output_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"
        output_dir = Path(output_path).joinpath(repo)
        if output_dir.exists() and output_dir.is_dir():
            shutil.rmtree(output_dir)



        command = [
            "nohup",
            "python3",
            "command.py",
            "-r",
            repo_path,
            "-c", "1",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}1.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        command = [
            "nohup",
            "python3",
            "command.py",
            "-r",
            repo_path,
            "-c", "2",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}2.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        command = [
            "nohup",
            "python3",
            "command.py",
            "-r",
            repo_path,
            "-c", "3",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}3.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        command = [
            "nohup",
            "python3",
            "command.py",
            "-r", repo_path,
            "-c", "4",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}4.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        command = [
            "nohup",
            "python3",
            "command.py",
            "-r", repo_path,
            "-c", "5",
            "-o",
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/",
            "-p", "local"
        ]
        print("running command: ", command)
        with open(f"run_log/{repo}5.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("2").joinpath("refs").glob("*.json")]
        # assert len(jsons_refs) == 5
        jsons_refs = [each for each in dir_path.joinpath("3").joinpath("refs").glob("*.json")]
        # assert len(jsons_refs) == 2

        # Trace
        command = [
            "nohup",
            "python3",
            "command.py",
            "-m",
            "trace",
            "-r", repo_path,
            "-d",
            f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/{repo}/",
            "--start",
            "2",
            "--end",
            "5"
        ]
        print("running command: ", command)
        with open(f"run_log/so_tr_{repo}.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("o2").rglob("*.json")]
        # assert len(jsons_refs) == 10

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("o3").rglob("*.json")]
        # assert len(jsons_refs) == 8

        # Retrace
        command = ["python3",
                   "retrace.py",
                   "-t",
                   f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/{repo}/",
                   "-r", repo_path,
                   ]
        print("running command: ", command)
        with open(f"run_log/retrace_{repo}.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

        dir_path = Path(output_path).joinpath(repo)
        jsons_refs = [each for each in dir_path.joinpath("retrace").rglob("*.json")]
        # assert len(jsons_refs) == 5