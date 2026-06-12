import sys
import subprocess
import argparse
import json
from unittest import case

def main():
    parser = argparse.ArgumentParser(
        prog='Yo Git Tools',
        description='Simplified git process tools')
    parser.add_argument('command', 
                        choices=['nuke', 'new', 'fetch', "pull", "push", "pr", "merge"])
    args = parser.parse_args()
    settings = load_settings()
    match args.command:
        case "nuke":
            return nuke()
        case "new":
            return new(settings, args)
        case "fetch":
            return fetch(settings)
        case "pull":
            return pull()
        case "push":
            return push()
        case "pr":
            return pr()
        case "merge":
            return merge()
    return 1

def load_settings():
    with open(".yosettings.json") as json_file:
        settings = json.load(json_file)
        return settings

def nuke():
    result = run(["git", "stash", "push", "--include-untracked"])
    return result

def new(settings, args):
    run(["git", "stash", "push", "--include-untracked"])
    run(["git", "fetch", "--prune"])
    run(["git", "switch", f"origin/{settings["default-branch"]}", "--detach"])
    return run(["git", "switch", "-c", args.argument_one])

def fetch(settings):
    run(["git", "fetch", "--prune", "--progress"])
    return run(["git", "lfs", "fetch", "origin", settings["default-branch"]])

def pull():
    # foreach local branch merge latest develop
    print("not implemented yet")
    return 1

def push():
    run(["git", "add", "."])
    run(["git", "commit", "-a", "--allow-empty-message", "-m", "\'\'"])
    return run(["git", "push"])

def pr():
    print("not implemented yet")
    return 1


def merge():
    print("not implemented yet")
    return 1


def run(arr):
    print(arr)
    proc = subprocess.run(arr)
    return proc.returncode

if __name__ == '__main__':
    try:
        return_code = main()
    except Exception as e:
        print(e)
        return_code = 1
    sys.exit(return_code)
