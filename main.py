import sys
import subprocess
import argparse
import json

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
    run(["git", "stash", "push", "--include-untracked"])
    run(["git", "fetch", "--prune"])
    run(["git", "switch", f"origin/{settings["default-branch"]}", "--detach"])
    return run(["git", "switch", "-c", args.branch_name])

def fetch(settings, args):
    run(["git", "fetch", "--prune", "--progress"])
    return run(["git", "lfs", "fetch", "origin", settings["default-branch"]])

def pull(settings, args):
    # foreach local branch merge latest develop
    # Source: https://stackoverflow.com/questions/3408532/merging-without-changing-the-working-directory

    # git for-each-ref --format='%(refname:short)' refs/heads/
    b = run_and_get_output(["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"])
    branches = b.splitlines()
    print(branches)
    
    default = settings["default-branch"]
    
    for branch in branches:
        if branch == default:
            continue
            
        if run_and_get_output(["git", "merge-base", branch, default]).strip() == run_and_get_output(["git", "rev-parse", default]).strip():
            tree = run_and_get_output(["git", "log", "-n", "1", "--pretty=%T", branch]).strip()
            process = subprocess.run(["git", "commit-tree", tree, "-p", default, "-p", branch], input=f'Merge branch {branch}'.encode('utf-8'), stdout=subprocess.PIPE)
            new_commit = process.stdout.decode('utf-8').strip()
            run_and_get_output(["git", "update-ref", "-m", f"merge {branch}: Merge made by simulated no-ff", f"refs/heads/{default}", new_commit])
# make the commit
# newcommit=$(echo "Merge branch '$currentbranch'" | git commit-tree $(git log -n 1 --pretty=%T HEAD) -p $branch -p HEAD)
# move the branch to point to the new commit
# git update-ref -m "merge $currentbranch: Merge made by simulated no-ff" "refs/heads/$branch" $newcommit
        else:
            print(f"cant ff {branch}")
    return 0

def push(settings, args):
    run(["git", "add", "."])
    run(["git", "commit", "-a", "--allow-empty-message", "-m", "\'\'"])
    return run(["git", "push"])

def pr(settings, args):
    print("not implemented yet")
    return 1


def merge(settings, args):
    print("not implemented yet")
    return 1


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
