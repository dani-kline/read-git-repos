# read-git-repos
CLI Tool that accepts a git URL or a GitHub Organization and outputs a JSON file with the number of manifest files scannable by Snyk per repo. 
- Read repo and output manifest file count (when using `--gitrepo` flag)
- Read GitHub Organization and output manifest file count per repo (when using `--githuborg` flag)

### Requirements
* Python (version 3.10.8 used to test)

### Known Limitations
* If a manifest file is not defined in [manifest_count_dict](https://github.com/dani-kline/read-git-repos/blob/502278db69dc8a65ac7a9a6f3e6bc064a44fb25e/scan-repo.py#L9-L26) it will not be counted.
* Currently will count manifest files per repo in GitHub organizations, but cannot in BitBucket Teams or GitLab Groups.

### Usage
1. _Clone this repo locally 
2. _Install the requirements from the requirements.txt `pip install -r requirements.txt`

```
Usage: python scan-repo.py [OPTIONS] [GITDEFAULTBRANCH] [OUTPUTFILE] [GHTOKEN]
                
                Either --gitrepo or --githuborg must be specified. 

Arguments: 
  gitdefaultbranch      [GITDEFAULTBRANCH]  Default branch for the repo, required if getting manifest files within a repo. [env var: DEFAULT_BRANCH] [default: main]
  outputfile            [OUTPUTFILE]        The name of the json file to output manifest file counts in the root directory. [default: manifestcount.json]
  ghtoken               [GHTOKEN]           Github Personal Access Token, required if getting manifest files within a GitHub Org. [env var: GITHUB_TOKEN]

Options:
  --gitrepo             If getting manifest files for a repo, enter the git url with this option [default: None]
  --githuborg           If getting manifest files for repos within a GitHub org, enter the name of the GitHub Organization with this option. [default: None]
  --help                Show help                                      [boolean]
```

__Example__: 
```
python scan-repo.py --gitrepo 'https://github.com/dani-kline/read-git-repos.git' 
```

### Contributing
See guidelines [here](.github/CONTRIBUTING.md)

### Further Exploration
1. _Setup with [GitHub Python library](https://github.com/PyGithub/PyGithub) to use the GitHub Python Package to simplify getting the repos in a GitHub Org and getting the git tree.
2. _Output additional information such as: repos found, and per repo--languages, Snyk webhooks, default branch
