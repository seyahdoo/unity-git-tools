git nuke -> remove all untracked files, discard all changes (alt + delete) and (alt + w)? maybe
  git stack everything
	? - git clean -f
	? - git restore .


git new branch-name -> switch to new branch (alt + n)
	git fetch --prune
	git checkout -b new-branch-name origin/develop


git prep -> fetch all new lfs files and commits (alt + delete)
	git fetch --prune
	git lfs fetch --recent
	

git down -> rebase all local branches with develop (alt + r)
	foreach local branch other than develop
		git pull


git up -> commit everything and push all local branches (alt + s)
  	git commit -a --allow-empty-message -m ''
	git down
	git push



git config --global alias.nuke "!git clean -f && git restore ."
git config --global alias.new "!git fetch --prune && git switch -c $1 origin/develop"


