import subprocess
from chatfreept import ChatFreePT
from sys import argv

# Constants
IS_HEADLESS = "--headless" in argv
IS_LOG = "--log" in argv
GAC_PREFIX = "[gac] "
PROMPT = """PROMPT:
Your task is to create a standardized commit message using Git diff logs.
Description:
Given a Git diff log, your objective is to convert it into a commit message that follows the conventional style.
The commit message should begin with a type (such as feat, fix, docs, refactor, test, chore, style, perf, ci, revert).
The commit message should describe how/why you made the changes in the commit. Prioritize why over how.
Ensure that the commit message is concise and easy to understand.

(Note: Provide only the standardized commit message without any additional context, explanations, or queries.)

Git Diff Log
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
        if not result.returncode == 0:
            print(result.stderr)
            return None
        return result.stdout.strip()

    def get_diff_logs(self):
        diff_logs = self.run(["git", "diff", "--staged"])
        if not diff_logs:
            raise ValueError("No git diff --staged changes found.")
        return diff_logs

    def commit(self, message):
        prefixed_message = f"{GAC_PREFIX}{message}"
        response = self.run(["git", "commit", "-m", prefixed_message])
        print(response)


def main():
    print(f"Starting... --headless={IS_HEADLESS} --log={IS_LOG}")
    freept = ChatFreePT(headless=IS_HEADLESS, log=IS_LOG)
    git_cli = GitCLI()

    print("Getting diff logs...")
    diff_logs = git_cli.get_diff_logs()

    print("Asking GPT for a commit message...")
    commit_message = freept.chat(f"{PROMPT} {diff_logs}")

    print("Committing...")
    git_cli.commit(commit_message)

    freept.close()


if __name__ == "__main__":
    main()
