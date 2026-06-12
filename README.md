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
