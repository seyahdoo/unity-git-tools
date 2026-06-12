import sys
import subprocess
import argparse
import json
import requests

def main():
    parser = argparse.ArgumentParser(
        prog='Yo Git Tools',
        description='Simplified git process tools')

    subparsers = parser.add_subparsers(help='command')

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

    parser_commit = subparsers.add_parser('commit', help='commit everything and push to current branch')
    parser_commit.set_defaults(func=push)

    parser_pr = subparsers.add_parser('pr', help='make new pr from current branch to default branch')
    parser_pr.add_argument('pr_title')
    parser_pr.set_defaults(func=pr)

    parser_merge = subparsers.add_parser('merge', help='squash merge current branch to default branch')
    parser_merge.set_defaults(func=merge)
    
    args = parser.parse_args()
    return args.func(args)

def nuke(args):
    result = run(["git", "stash", "push", "--include-untracked"])
    return result

def new(args):
    default_branch = get_default_branch()
    run(["git", "fetch", "--prune"])
    run(["git", "switch", f"origin/{default_branch}", "--detach"])
    return run(["git", "switch", "-c", args.branch_name])

def fetch(args):
    default_branch = get_default_branch()
    run(["git", "fetch", "--prune", "--progress"])
    return run(["git", "lfs", "fetch", "origin", default_branch])

def pull(args):
    default_branch = get_default_branch()
    fetch(args)
    run(["git", "merge", f"origin/{default_branch}", "--no-edit"])
    run(["git", "push"])

def push(args):
    run(["git", "add", "."])
    run(["git", "commit", "-a", "--allow-empty-message", "-m", "\'\'"])
    return run(["git", "push"])

def pr(args):
    token = get_github_access_token()
    default_branch = get_default_branch()
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

def merge(args):
    token = get_github_access_token()
    default_branch = get_default_branch()
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

def get_default_branch():
    default = run_and_get_output(["git", "config", "yo.default-branch"]).strip()
    if default:
        return default
    return "develop"

def get_github_access_token():
    pat = run_and_get_output(["git", "config", "yo.github-access-token"]).strip()
    if pat:
        return pat
    return ""

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
