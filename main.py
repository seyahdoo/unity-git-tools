import os
import sys
import subprocess
import argparse
import json

def main():
    parser = argparse.ArgumentParser(
        prog='Yo Git Tools',
        description='Simplified git process tools')
    parser.add_argument('command')
    parser.add_argument('argument_one', required=False)
    # parser.add_argument('-c', '--count')      # option that takes a value
    # parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag

    args = parser.parse_args()

    with (open(".yosettings.json", mode="r", encoding="utf-8") as file):
        settings = json.load(file)
    
    if args.command == "nuke":
        result = run(["git", "stash", "push", "--include-untracked"])
        return result.returncode
    
    if args.command == "new":
        run(["git", "stash", "push", "--include-untracked"])
        run(["git", "fetch", "--prune"])
        run(["git", "switch", f"origin/{settings["default-branch"]}", "--detach"])
        result = run(["git", "switch", "-c", args.argument_one])
        return result.returncode


    return 1

def run(arr):
    print(arr)
    proc = subprocess.Popen(arr, shell=False)
    proc.communicate()
    return proc.returncode

if __name__ == '__main__':
    try:
        return_code = main()
    except Exception:
        return_code = 1
    sys.exit(return_code)
