import subprocess
from chatfreept import ChatFreePT
from sys import argv

# Constants
IS_DEBUG = "--debug" in argv
GAC_PREFIX = "[gac] "
PROMPT = """PROMPT:
Your name is [gac], which stands for Git-AI-Commit. Your task is to convert Git Diff Logs to Standardized Commit Messages.
DESCRIPTION:
Given a Git diff log, your goal is to transform it into standardized commit messages adhering to the conventional commit message style.
Each commit message should start with a type (e.g., feat, fix, docs, refactor, test, chore, style, perf, ci, revert) followed by a description of the changes made in the commit. Keep the commit messages short and simple.
(Note: Only provide the standardized commit message without any introductions, explanations, or questions.)
GIT DIFF LOG:
"""


class GitCLI:
    def __init__(self):
        self.subprocess_runner = subprocess.run

    def run(self, command):
        result = self.subprocess_runner(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(result.stderr)
            return None

    def get_diff_logs(self):
        diff_logs = self.run(["git", "diff", "--staged"])
        if diff_logs:
            return diff_logs
        else:
            raise ValueError("No git diff --staged changes found.")

    def commit(self, message):
        prefixed_message = f"{GAC_PREFIX}{message}"
        response = self.run(["git", "commit", "-m", prefixed_message])
        print(response)


def main():
    print("Starting...")
    freept = ChatFreePT(debug=IS_DEBUG)
    git_cli = GitCLI()

    print("Getting diff logs...")
    diff_logs = git_cli.get_diff_logs()

    print("Asking GPT for a commit message...")
    commit_message = freept.chat(f"{PROMPT} {diff_logs}")

    print("Committing...")
    git_cli.commit(commit_message)


if __name__ == "__main__":
    main()
