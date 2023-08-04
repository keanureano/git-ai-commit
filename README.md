# Git AI Commit

---

## Introduction

Python script that automatically generates commit messages based on git added files.
The generated commit message can be accepted or modified before committing.

## Usage Instructions

1. Install Requirements: Before executing the script, make sure to install all dependencies listed in the requirements.txt file by running the following command:

```
pip install -r requirements.txt
```

2. Register at [HuggingFace](https://huggingface.co), rename `.env.example -> .env`, fill out the environment variables.

```
EMAIL="example@gmail.com"
PASSWORD="example"
```

3. Open up VS Code terminal and type

```
code $profile
```

4. A text editor should pop up. Copy paste this function and replace `<FILE_PATH>`

```
function gac {
    py "<FILE_PATH>\main.py"
}
```

5. After closing and reopening VS Code, you should be able to just type this in the terminal.

```
git add <file(s)>
gac
```

## Functionality

The following sections describe the various components of the script and their respective roles:

- **`git_diff()`**: Retrieves the current staged diff logs using the `git diff --staged` command.
- **`generate_commit_message()`**: Interacts with the Hugging Face API chatbot to generate a concise commit message based on the provided Git diff logs. The user is prompted to confirm whether to proceed with committing the changes or retry. If confirmed, the generated commit message is printed and used as the basis for the next iteration. Otherwise, the process continues without committing any changes.
- **`git_commit()`**: Runs the `git commit` command with the specified message passed as an argument. If successful, the standard output is printed; otherwise, the error message is logged.
