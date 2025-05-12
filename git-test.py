# https://github.com/anselbrandt/prefect-demo

import os
from git import Repo
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN not found in .env")

repo_path = Path.cwd()
file_path = repo_path / "hello.txt"

with open(file_path, "w") as f:
    f.write("hello world\n")

repo = Repo(repo_path)
assert not repo.bare

with repo.config_writer() as git_config:
    git_config.set_value("user", "name", "anselbrandt")
    git_config.set_value("user", "email", "ansel@anselbrandt.com")

repo.git.add("hello.txt")
repo.index.commit("Add hello.txt")

origin = repo.remote(name="origin")
remote_url = origin.url

if remote_url.startswith("https://"):
    authed_url = remote_url.replace("https://", f"https://{token}@")
else:
    raise ValueError("Only HTTPS remote URLs are supported")

origin.set_url(authed_url)
origin.push()

origin.set_url(remote_url)

print("Committed and pushed successfully.")
