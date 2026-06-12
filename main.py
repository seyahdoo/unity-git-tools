import sys
import subprocess
import argparse
import json

import requests


def main():
    settings = load_settings()
    
    parser = argparse.ArgumentParser(
        prog='Yo Git Tools',
        description='Simplified git process tools')

    subparsers = parser.add_subparsers(help='command')

    parser_clone = subparsers.add_parser('clone', help='clone new repo')
    parser_clone.set_defaults(func=clone)

    parser_nuke = subparsers.add_parser('nuke', help='clean the workplace non-destructively')
    parser_nuke.set_defaults(func=nuke)

    parser_new = subparsers.add_parser('new', help='creates a new branch from origin default and checks out')
    parser_new.add_argument('branch_name')
    parser_new.set_defaults(func=new)

    parser_fetch = subparsers.add_parser('fetch', help='fetch all data from newest default branch')
    parser_fetch.set_defaults(func=fetch)

    parser_pull = subparsers.add_parser('pull', help='update all local branches and workspace with newest default branch')
    parser_pull.set_defaults(func=pull)

    parser_push = subparsers.add_parser('push', help='commit everything and push to current branch')
    parser_push.set_defaults(func=push)

    parser_pr = subparsers.add_parser('pr', help='make new pr from current branch to default branch')
    parser_pr.add_argument('pr_title')
    parser_pr.set_defaults(func=pr)

    parser_merge = subparsers.add_parser('merge', help='squash merge current branch to default branch')
    parser_merge.set_defaults(func=merge)
    
    args = parser.parse_args()
    return args.func(settings, args)

def load_settings():
    try:
        with open(".yosettings.json") as json_file:
            settings = json.load(json_file)
            return settings
    except FileNotFoundError:
        return {"default-branch": "develop"}

def clone(settings, args):
    print("not implemented yet")
    return 1

def nuke(settings, args):
    result = run(["git", "stash", "push", "--include-untracked"])
    return result

def new(settings, args):
    run(["git", "fetch", "--prune"])
    run(["git", "switch", f"origin/{settings["default-branch"]}", "--detach"])
    return run(["git", "switch", "-c", args.branch_name])

def fetch(settings, args):
    run(["git", "fetch", "--prune", "--progress"])
    return run(["git", "lfs", "fetch", "origin", settings["default-branch"]])

def pull(settings, args):
    default = settings["default-branch"]
    fetch(settings, args)
    run(["git", "merge", f"origin/{default}", "--no-edit"])
    run(["git", "push"])

def push(settings, args):
    run(["git", "add", "."])
    run(["git", "commit", "-a", "--allow-empty-message", "-m", "\'\'"])
    return run(["git", "push"])

def pr(settings, args):
    token = get_github_auth()
    default_branch = settings["default-branch"]
    pr_title = args.pr_title
    current_branch = run_and_get_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()

    if current_branch == default_branch:
        print("Cannot merge default branch to itself")
        return 1
    
    origin_url = run_and_get_output(["git", "config", "--get", "remote.origin.url"]).strip()
    if not origin_url.startswith("git@github.com:"):
        print("Not a GitHub repository, will not create a pr")
        return 1
    repo_id = origin_url.removeprefix("git@github.com:").removesuffix(".git")
    
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2026-03-10',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    data = {
        "title": pr_title,
        "head": current_branch,
        "base": default_branch
    }
    
    response = requests.post(f'https://api.github.com/repos/{repo_id}/pulls', headers=headers, data=json.dumps(data))
    if response.status_code != 201:
        print("Error when creating pull request")
        print(response.json()["errors"][0]["message"])
        return 1
    
    print("Pull request created successfully")
    return 0

def get_github_auth():
    with open(".yoauth.json") as json_file:
        auth = json.load(json_file)
        return auth["github-access-token"]

def merge(settings, args):
    token = get_github_auth()
    default_branch = settings["default-branch"]
    current_branch = run_and_get_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()
    
    if current_branch == default_branch:
        print("Cannot merge default branch to itself")
        return 1

    origin_url = run_and_get_output(["git", "config", "--get", "remote.origin.url"]).strip()
    if not origin_url.startswith("git@github.com:"):
        print("Not a GitHub repository, will not merge a pr")
        return 1
    repo_id = origin_url.removeprefix("git@github.com:").removesuffix(".git")

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2026-03-10',
    }
    response = requests.get(f'https://api.github.com/repos/{repo_id}/pulls', headers=headers)

    j = response.json()
    pr_number = -1
    for pr in j:
        if pr["head"]["ref"] == current_branch:
            pr_number = pr["number"]

    if pr_number == -1:
        print("PR has not been found. Please create PR with \"yo pr [title]\"")
        return 1

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2026-03-10',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"merge_method":"squash"}'
    response = requests.put(f'https://api.github.com/repos/{repo_id}/pulls/{pr_number}/merge', headers=headers, data=data)
    if response.status_code != 200:
        print("Error when merging pull request")
        print(response.json()["message"])
        return 1
    
    print(response.json()["message"])
    run(["git", "fetch", "--prune", "--progress"])
    run(["git", "fetch", "origin", f"{default_branch}:{default_branch}"])
    run(["git", "checkout", default_branch])
    run(["git", "branch", "-D", current_branch])
    run(["git", "fetch", "--prune", "--progress"])
    return 0


def run(arr):
    print(arr)
    proc = subprocess.run(arr)
    return proc.returncode

def run_and_get_output(args):
    print(args)
    result = subprocess.run(args, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return output

if __name__ == '__main__':
    try:
        return_code = main()
    except Exception as e:
        print(e)
        return_code = 1
    sys.exit(return_code)
