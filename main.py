import argparse
import os

from dotenv import load_dotenv

from gitcopilot.git import Repository
from gitcopilot.gpt import Copilot


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Process git commits between two branches."
    )
    parser.add_argument("--before", required=True, help="Name of the before branch.")
    parser.add_argument("--after", required=True, help="Name of the after branch.")
    parser.add_argument("--version", required=True, help="Version name.")
    args = parser.parse_args()

    repo_path = os.getenv("GIT_REPOSITORY_PATH")
    if not repo_path:
        print("Please set GIT_REPOSITORY_PATH in .env file")
        exit(1)

    repo = Repository(repo_path)
    copilot = Copilot()

    commit_infos = repo.generate_commit_data(args.before, args.after)
    df = repo.generate_to_data_frame(args.before, args.after)
    df.to_csv(f"data/{args.version}.csv", index=False)

    for value in df["message"].values:
        print(value, end="======================================\n\n")

    result = copilot.summarize_commits(commit_infos, "prompts/summarize_commits.md")
    if result:
        print(result)
        with open(f"data/{args.version}.md", "w", encoding="utf-8") as f:
            f.write(result)


if __name__ == "__main__":
    main()
