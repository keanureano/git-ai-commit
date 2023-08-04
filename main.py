import os
from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv
import subprocess


def main():
    staged_diff_logs = git_diff()
    commit_message = generate_commit_message(staged_diff_logs)
    git_commit(commit_message)


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


def generate_commit_message(staged_diff_logs):
    while True:
        load_dotenv()
        EMAIL = os.getenv("EMAIL")
        PASSWORD = os.getenv("PASSWORD")
        hugging_face_login = Login(EMAIL, PASSWORD)

        cookies = hugging_face_login.login()
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

        prompt = f"""
        Task: Generate a concise commit message based on the given Git diff logs.
        Do not include any additional information or explanations. Only the command should be given.

        Git diff logs:
        ```
        {staged_diff_logs}
        ```
        """

        commit_message = chatbot.chat(prompt)
        print("\033[92m" + commit_message + "\033[0m")

        response = input("Confirm commit? [Y]es/[R]etry: ")

        if response == "y":
            return commit_message
        else:
            continue


def git_commit(message):
    result = subprocess.run(
        ["git", "commit", "-m", message],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(result.stderr)
        return None


if __name__ == "__main__":
    main()
