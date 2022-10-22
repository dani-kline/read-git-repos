# read-git-repos

TODO:
1. (FIRST) Setup this project with pip python
2. Setup the project with github python library - https://github.com/PyGithub/PyGithub
2. (FIRST) Commandline accept parameter : "python scan-repo.py -gitrepo 'https://github.com/huytquach-snyk/read-git-repos)' "
3. Function inside will scan the repo and check it exist - use the github python package
4. (FIRST) User "git clone" pull repo - See sample - get_git_tree_from_clone - https://github.com/huytquach-snyk/read-git-repos/blob/main/scan-repo.py#L3 - make sure you download it tmp folder
5. (FIRST) Then use the pattern https://github.com/huytquach-snyk/read-git-repos/blob/main/scan-repo.py#L1 to find all the files needed in this downloaded repo - Need a data structure to store all results
6. (FIRST) From the data structure in 5, serialize to JSON.

Pip (v3) Python (v3)
https://www.geeksforgeeks.org/how-to-install-pip-in-macos/

Commandline lib; - use easiest one - goos example
Python Fire	Library for automatically generating command line interfaces
argparse	Parser for command-line options, arguments and sub-commands
Click	Create beautiful command line interfaces in a composable way
Gooey	Convert console programs into end-user-friendly GUI software

Github Python;
https://github.com/PyGithub/PyGithub
