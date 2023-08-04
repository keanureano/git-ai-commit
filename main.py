import subprocess


def main():
    staged_diff_logs = git_diff()


def git_diff():
    result = subprocess.run(
        ["git", "diff", "--staged"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout
    else:
        print(result.stderr)
        return None
