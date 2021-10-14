from github import Github
from github.InputGitTreeElement import InputGitTreeElement
from github.Repository import Repository
import json
import os
import io
import base64

def updateHistory(repo: Repository, name: str, contents: dict) -> None:
    commit_message = "Automatic commit"
    master_ref = repo.get_git_ref("heads/master")
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = []
    element = InputGitTreeElement(name, '100644', 'blob', json.dumps(contents, indent=2))
    element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
    
    return None

def get_repo():
    key = os.getend("key")
    if not key:
        key = input("Input key: ")

    with io.open("tokens.json", mode="r", encoding="utf-8") as f:
        tokens = json.load(f)

    github_token_encoded = tokens["github_token"]
    github_token_decoded = "".join(tuple([chr(ord(github_token_encoded[i]) ^ ord(key[i % len(key)])) for i in range(len(github_token_encoded))]))

    g = Github(base64.b64decode(github_token_decoded).decode("utf-8"))
    repo = g.get_repo("alex-eliot/csd-rss")

    return repo