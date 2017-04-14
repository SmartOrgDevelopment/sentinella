class TravisNotice:
    def __init__(self, data):
        self.data = data

    def get_repo_name(self):
        return self.data["repository"]["name"]

    def get_branch_name(self):
        return self.data["branch"]

    def get_status(self):
        return str(self.data["status_message"]).lower()

    def get_committer_name(self):
        return self.data["committer_name"]

    def get_commit_time(self):
        return self.data["committed_at"]

    def get_data(self):
        return self.data
