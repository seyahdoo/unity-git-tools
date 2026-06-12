# TODO

git nuke -> remove all untracked files, discard all changes (ctrl + shift + delete) and (ctrl + shift + w)? maybe
  git stack everything
	? - git clean -f
	? -git restore .


git new branch-name -> switch to new branch (ctrl + shift + n)
	git fetch --prune
	git checkout -b new-branch-name origin/develop


git prep -> fetch all new lfs files and commits (ctrl + shift + delete)
	git fetch --prune
	git lfs fetch --recent
	

git down -> rebase all local branches with develop (ctrl + shift + r)
	foreach local branch other than develop
		git pull


git up -> commit everything and push all local branches (ctrl + shift + s)
  git commit
	git down
	git push



git config --global alias.nuke "!git clean -f && git restore ."
git config --global alias.new "!git fetch --prune && git switch -c $1 origin/develop"


