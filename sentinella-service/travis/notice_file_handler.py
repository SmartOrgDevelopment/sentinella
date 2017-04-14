import os
import json
from datetime import datetime

__REPORT_FOLDER = "travis_reports"


def __get_repo_folder_name(repo_name):
    return "{}/{}".format(__REPORT_FOLDER, repo_name)


def __get_branch_file_name(repo_name, branch_name):
    return "{}/{}/{}".format(__REPORT_FOLDER, repo_name, branch_name)


def __create_folder(repo_name):
    folder_name = __get_repo_folder_name(repo_name)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def __write_file(repo_name, branch_name, data):
    __create_folder(repo_name)
    file_path = __get_branch_file_name(repo_name, branch_name)

    with open(file_path, "w") as data_file:
        json.dump(data, data_file)


def write_timestamp():
    with open(__REPORT_FOLDER + "/timestamp", "w") as data_file:
        data_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def load_timestamp():
    with open(__REPORT_FOLDER + "/timestamp", "r") as data_file:
        return data_file.read()


def record_notice(folder_name, file_name, data):
    __write_file(folder_name, file_name, data)


def get_notice_list(repos):
    reports = []

    for repo in repos:
        repo_name = repo["id"]
        for branch in repo["branches"]:
            branch_path = __get_branch_file_name(repo_name, branch)

            if os.path.exists(branch_path):
                with open(branch_path) as data_file:
                    try:
                        reports.append(json.load(data_file))
                    except ValueError:
                        pass

    return reports
