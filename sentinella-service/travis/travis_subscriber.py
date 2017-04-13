import requests
import logging

from config.config import read_travis_config
from config.config import PASSED, FAILED
from travis_reports import write_report

logging.basicConfig(filename="travis.log")


class TravisSub(object):
    __TRAVIS_URI = "https://api.travis-ci.com"

    __GITHUB_AUTH_HEADER = {
        "User-Agent": "MyClient/1.0.0",
        "Accept": "application/vnd.travis-ci.2+json",
        "Host": "api.travis-ci.com",
        "Content-Type": "application/json"
    }

    @staticmethod
    def __analyse_status(rs):
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
        self.token, self.git_id, self.repos = read_travis_config()
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
        route = self.__make_branch_request_uri(repo, branch)

        try:
            rs = requests.get(TravisSub.__TRAVIS_URI + route,
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
            analyse_result = TravisSub.__analyse_status(report)
            if analyse_result == PASSED:
                write_report(report, PASSED)
            else:
                write_report(report, FAILED)
            return analyse_result
        else:
            logging.error("Failed to load travis token")
            return None
