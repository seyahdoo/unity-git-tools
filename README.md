```
yo nuke (stash all local changes and clean workspace)
yo new branch-name (make new branch from develop, checkout new branch)
yo fetch (fetch all data from newest develop)
yo pull (update current branche and workspace with newest develop)
yo push = yo commit (commit everything and push to branch) (will fail with message on develop)
yo pr title (make new pr from current branch to develop) (will fail with message on develop)
yo merge (squash merge current branch to develop) (will fail with message if pr does not exist, or on develop)
```
