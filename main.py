import sys
import subprocess
import argparse
import json

def main():    
    parser = argparse.ArgumentParser(
        prog='Yo Git Tools',
        description='Simplified git process tools')
    parser.add_argument('command')
    args = parser.parse_args()
    settings = load_settings()
    
    if args.command == "nuke":
        return nuke()
    
    if args.command == "new":
        return new(settings, args)

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
    result = run(["git", "switch", "-c", args.argument_one])
    return result

def run(arr):
    print(arr)
    # proc = subprocess.run(arr)
    return proc.returncode

if __name__ == '__main__':
    try:
        return_code = main()
    except Exception:
        return_code = 1
    sys.exit(return_code)
