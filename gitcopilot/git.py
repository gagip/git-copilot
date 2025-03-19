from git import Repo
import pandas as pd


class Repository:
    def __init__(self, repo_path: str) -> None:
        self.repo = Repo(repo_path)

    def generate_to_data_frame(self, before_branch_name: str, after_branch_name: str) -> pd.DataFrame:
        commit_data = []
        for commit in self.repo.iter_commits(f'{before_branch_name}..{after_branch_name}'):
            commit_info = {
                'commit_id': commit.hexsha,
                'author': f'{commit.author.name} <{commit.author.email}>',
                'datetime': commit.committed_datetime,
                'message': commit.message
            }
            commit_data.append(commit_info)
        
        return pd.DataFrame(commit_data)

    def generate_commit_data(self, before_branch_name: str, after_branch_name: str) -> str:
        commit_data = []
        for commit in self.repo.iter_commits(f'{before_branch_name}..{after_branch_name}'):
            commit_info = (
                f"Commit ID: {commit.hexsha}\n"
                f"Author: {commit.author.name} <{commit.author.email}>\n"
                f"Date: {commit.committed_datetime}\n"
                f"Message: {commit.message}"
            )
            commit_data.append(commit_info)
        
        return '\n\n'.join(commit_data)  # 각 커밋 정보를 두 개의 개행 문자로 구분
    
    def get_commit_info(self, branch_name: str) -> pd.DataFrame:
        commit_data = []
        for commit in self.repo.iter_commits(branch_name):
            commit_info = {
                'commit_id': commit.hexsha,
                'author': f'{commit.author.name} <{commit.author.email}>',
                'datetime': commit.committed_datetime,
                'message': commit.message
            }
            commit_data.append(commit_info)
        
        return pd.DataFrame(commit_data)