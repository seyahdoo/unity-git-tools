# Yo Git Client 
An extremely opinionated git client that just works if you work exacly like me.

- does not care about the commit messages on branch commits
- will make a branch and push if you try to commit on main branch
- tools to make and merge prs and auto switch back to main when pr merges

## [Download Release](https://raw.githubusercontent.com/seyahdoo/yo-git-tools/refs/heads/main/dist/yo.exe)

# Setup

- If you wanna use, yo pr and yo merge you have to setup github pat
- https://github.com/settings/personal-access-tokens
- Generate new token
- Permissions -> Contents (read and write), Pull requests (read and write), Metadata
- Then run this commands for the repo

  
```
git config set yo.default-branch "main"
git config set yo.github-access-token "github_pat_XXXXXXXXXXXXXXXX"
```

- You are now all set

# Commands

```
yo nuke
    stash all local changes and clean workspace

yo new branch-name
    make new branch from main, checkout new branch

yo fetch
    fetch all data from newest main

yo pull
    update current branche and workspace with newest main

yo push
    commit everything and push to branch

yo commit
    commit everything with an empty message, push to remote

yo pr title
    make new pr from current branch to main

yo merge
    squash merge current branch to main
```

# Unity Integration
- mission bar at the top, showing current branch name
- fetches every 15 minutes with lfs
- will show incoming changes if found fetch
- press to pull everything to curent branch
- ctrl alt shift s to make a blank commit on current branch, will make a new temp branch if on main
- ctrl alt shift z back to most recent commit
- ctl alt shift p make a pr
- crtl alt shift m merge current pr
- ctrl alt shift f fetch and pull changes to current branch
