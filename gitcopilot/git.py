from git import Commit, Repo
import pandas as pd
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CommitInfo:
    commit_id: str
    author: str
    datetime: datetime
    message: str


def _create_commit_info(commit: Commit) -> CommitInfo:
    commit_message = ""
    if isinstance(commit.message, bytes):
        commit_message = commit.message.decode("utf-8")
    elif isinstance(commit.message, str):
        commit_message = commit.message

    return CommitInfo(
        commit_id=commit.hexsha,
        author=f"{commit.author.name} <{commit.author.email}>",
        datetime=commit.committed_datetime,
        message=commit_message,
    )


class Repository:
    def __init__(self, repo_path: str) -> None:
        self.repo = Repo(repo_path)

    def generate_to_data_frame(
        self, 
        before_branch_name: str, 
        after_branch_name: str
    ) -> pd.DataFrame:
        commit_info_list = []
        for commit in self.repo.iter_commits(
            f"{before_branch_name}..{after_branch_name}"
        ):
            commit_info = _create_commit_info(commit)
            commit_info_list.append(commit_info)

        return pd.DataFrame(commit_info_list)

    def generate_commit_data(
        self, 
        before_branch_name: str, 
        after_branch_name: str
    ) -> str:
        commit_info_list = []
        
        commits = self.repo.iter_commits(
            f"{before_branch_name}..{after_branch_name}"
        )
        for commit in commits:
            commit_info = _create_commit_info(commit)
            commit_info_list.append(commit_info)

        return "\n\n".join(str(commit_info) for commit_info in commit_info_list)

    def get_commit_info(self, branch_name: str) -> pd.DataFrame:
        commit_info_list = []
        for commit in self.repo.iter_commits(branch_name):
            commit_info = _create_commit_info(commit)
            commit_info_list.append(commit_info)

        return pd.DataFrame(commit_info_list)
