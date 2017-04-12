import os
import json
import requests
import logging

logging.basicConfig(filename="travis.log")

__CONFIG_FILE = "config.json"
__TRAVIS_OUTPUT_PASSED = "travis_output_passed.json"
__TRAVIS_OUTPUT_FAILED = "travis_output_failed.json"

PASSED = "passed"
FAILED = "failed"


def read_config():
    with open(__CONFIG_FILE) as data_file:
        data = json.load(data_file)
    return data["token"], data["git_id"], data["repos"]


def write_result(data, status=PASSED):
    if status == PASSED:
        output_file = __TRAVIS_OUTPUT_PASSED
        try:
            os.remove(__TRAVIS_OUTPUT_FAILED)
        except OSError:
            pass
    else:
        output_file = __TRAVIS_OUTPUT_FAILED
        try:
            os.remove(__TRAVIS_OUTPUT_PASSED)
        except OSError:
            pass

    with open(output_file, "w") as outfile:
        json.dump(data, outfile)


class TravisSub(object):
    __TRAVIS_URI = "https://api.travis-ci.com"

    __GITHUB_AUTH_HEADER = {
        "User-Agent": "MyClient/1.0.0",
        "Accept": "application/vnd.travis-ci.2+json",
        "Host": "api.travis-ci.com",
        "Content-Type": "application/json"
    }

    @staticmethod
    def analyse_status(rs):
        analyse_result = PASSED

        for repo, branches in rs.items():
            for branch_report in branches:
                branch = branch_report["branch"]

                if branch["state"] == FAILED:
                    analyse_result = FAILED
                break

            if analyse_result == FAILED:
                break

        return analyse_result


    def __init__(self):
        self.token, self.git_id, self.repos = read_config()
        self.travis_header = {
            "User-Agent": "MyClient/1.0.0",
            "Accept": "application/vnd.travis-ci.2+json",
            "Host": "api.travis-ci.com",
            "Authorization": ""
        }

    def __get_travis_token(self):
        github_token = {"github_token": self.token}

        try:
            rs = requests.post(TravisSub.__TRAVIS_URI + "/auth/github",
                               headers=TravisSub.__GITHUB_AUTH_HEADER,
                               params=github_token)

            self.travis_header["Authorization"] = "token {}".format(
                rs.json()["access_token"])
            return True
        except Exception as ex:
            logging.error(ex)
            return False

    def __make_branch_request_uri(self, repo, branch):
        return "/repos/{}/{}/branches/{}".format(self.git_id, repo, branch)

    def __get_branch_status(self, repo, branch):
        p = self.__make_branch_request_uri(repo, branch)

        try:
            print TravisSub.__TRAVIS_URI + p
            rs = requests.get(TravisSub.__TRAVIS_URI + p,
                              headers=self.travis_header)
            return rs.json()
        except Exception as ex:
            logging.error(ex)
            return None

    def __get_repo_status(self, repo):
        rs = []
        for b in repo["branches"]:
            rs.append(self.__get_branch_status(repo["id"], b))
        return rs

    def __get_all_project_status(self):
        rs = {}
        for repo in self.repos:
            rs[repo["id"]] = self.__get_repo_status(repo)
        return rs

    def generate_report(self):
        if self.__get_travis_token():
            report = self.__get_all_project_status()
            write_result(report)
            return TravisSub.analyse_status(report)
        else:
            logging.error("Failed to load travis token")
            return None
