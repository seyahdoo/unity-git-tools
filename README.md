```

git nuke -> remove all untracked files, discard all changes (alt + delete) and (alt + w)? maybe
git new branch-name -> switch to new branch from develop (alt + t)
git prep -> fetch all new lfs files and commits (alt + f)
git down -> rebase all local branches with develop (alt + r)
git up -> commit everything and push all local branches (alt + s)

[alias]
	nuke = !git stash push --include-untracked
	new = !git fetch --prune && git switch origin/develop --detach && git switch -c
	up = !git add . && git commit -a --allow-empty-message -m '' && git down && git push
	down = !git pull
	prep = !git fetch --prune --progress && git lfs fetch origin develop


```

```
yo clone (clone new repo for completeness sake, equals git clone)
yo nuke (stash all local changes and clean workspace)
yo new branch-name (make new branch from develop)
yo fetch (fetch all data from newest develop)
yo pull (update all local branches and workspace with newest develop)
yo push = yo commit (commit everything and push to branch) (will fail with message on develop)
yo pr title (make new pr from current branch to develop) (will fail with message on develop)
yo merge (squash merge current branch to develop) (will fail with message if pr does not exist, or on develop)
```
