import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='Yo Git Tools',
        description='Simplified git process tools')
    parser.add_argument('command')
    # parser.add_argument('-c', '--count')      # option that takes a value
    # parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag

    args = parser.parse_args()
    
    if args.command == "clone":
        result = subprocess.run(["git", "clone", sys.argv[2:]])
        return result.returncode
    
    if args.command == "nuke":
        result = subprocess.run(["git", "stash", "push", "--include-untracked"])
        return result.returncode
    
    return 1

if __name__ == '__main__':
    try:
        return_code = main()
    except Exception:
        return_code = 1
    sys.exit(return_code)
