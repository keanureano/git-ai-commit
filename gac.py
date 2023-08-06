import subprocess
from chatfreept import ChatFreePT

DEBUG = False
WORD_COUNT_LIMIT = 1000
GAC_PREFIX = "[gac] "
PROMPT = """PROMPT:
Your name is [GAC], which stands for Git-AI-Commit. Your task is to convert Git Diff Logs to Standardized Commit Messages
DESCRIPTION:
Given a Git diff log, your goal is to transform it into standardized commit messages adhering to the conventional commit message style. Each commit message should start with a type (e.g., feat, fix, docs, refactor, test, chore, style, perf, ci, revert) followed by a description of the changes made in the commit. Keep the commit messages short and simple.
(Note: Only provide the standardized commit message without any introductions, explanations, or questions.)
GIT DIFF LOG:
"""


class PowerShellCLI:
    def run(self, command):
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(result.stderr)
            return None

    def get_diff_logs(self):
        diff_logs = self.run(["git", "diff", "--staged"])
        if not diff_logs.strip():
            raise ValueError("No git diff --staged changes found.")
        diff_logs = " ".join(diff_logs.split()[:WORD_COUNT_LIMIT])
        return diff_logs

    def commit(self, message):
        prefixed_message = f"{GAC_PREFIX}{message}"
        response = self.run(["git", "commit", "-m", prefixed_message])
        print(response)


if __name__ == "__main__":
    freept = ChatFreePT(headless=not DEBUG)
    cli = PowerShellCLI()
    diff_logs = cli.get_diff_logs()

    commit_message = freept.chat(f"{PROMPT} {diff_logs}")
    cli.commit(commit_message)
