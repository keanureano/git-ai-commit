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