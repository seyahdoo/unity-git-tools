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
yo nuke (stash all local changes and clean workspace)
yo new branch-name (make new branch from develop, checkout new branch)
yo fetch (fetch all data from newest develop)
yo pull (update current branche and workspace with newest develop)
yo push (commit everything and push to branch)
yo commit (commit everything with an empty message, push to remote)
yo pr title (make new pr from current branch to develop)
yo merge (squash merge current branch to develop)
```
