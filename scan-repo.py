
from asyncio.subprocess import PIPE
import subprocess
import re
import json
import typer
import requests

MANIFEST_PATTERN_SCA = '^(?![.]).*(package[.]json|Gemfile[.]lock|pom[.]xml|build[.]gradle|.*[.]lockfile|build[.]sbt|.*req.*[.]txt|Gopkg[.]lock|go[.]mod|vendor[.]json|packages[.]config|.*[.]csproj|.*[.]fsproj|.*[.]vbproj|project[.]json|project[.]assets[.]json|composer[.]lock|Podfile|Podfile[.]lock)$'
manifest_count_dict = {
    "yarn.lock": 0,
    "package-lock.json": 0,
    "package.json": 0,
    "Gemfile.lock": 0,
    "pom.xml": 0,
    "build.gradle": 0,
    "build.sbt": 0,
    "Pipfile": 0,
    "requirements.txt": 0,
    "Gopkg.lock": 0,
    "vendor.json" : 0,
    "project.assets": 0,
    "packages.config": 0,
    "composer.lock": 0,
    "go.mod": 0
    }

def get_repos_given_org(git_org, ghtoken):
    """
    Uses GH API to get list of repos for get_manifest_from_clone
    """
    baseghurl = 'https://api.github.com/orgs/'
    getreposurl = ''.join([baseghurl,str(git_org),'/repos'])
    getreposheader = {'Authorization': 'token' + ghtoken }
    ghrepos = requests.get(getreposurl, headers=getreposheader).json()
    return ghrepos

def get_manifest_from_clone(repo_name, origin):
    """
    get git tree for large repos by performing
    a shallow clone 'git clone --depth 1'
    """

    # check if git exists on the system
    subprocess.run(["command", "-v", "git"], check=True, stdout=subprocess.DEVNULL)

    name = "test"
    clone_url = repo_name
    default_branch = origin

    GIT_CLONE_PATH = f"/tmp/{name}"

    # check that GIT_CLONE_PATH is set safely for deletion

    print(f"  - shallow cloning {name} from {clone_url} to {GIT_CLONE_PATH}")

    # clone the repo locally
    subprocess.run(["rm", "-fr", f"{GIT_CLONE_PATH}"], check=True)
    subprocess.run(
        ["git", "clone", "--depth", "1", clone_url, GIT_CLONE_PATH],
        check=True
    )

    print("  - Searching for manifest")

    # for manifest_name in manifest_count_dict:
    #     print(manifest_name)
        
    #     #find . -name "*package.json*" | wc -l - to find all files with that name - we may want to change to git_tree?
    #     proc1 = subprocess.Popen(
    #         [
    #             "find",
    #             GIT_CLONE_PATH,
    #             "-name",
    #             manifest_name,
    #         ],
    #         stdout=subprocess.PIPE
    #     )
    #     proc2 = subprocess.Popen(
    #         [
    #             "wc",
    #             "-l"
    #         ],
    #         stdin=proc1.stdout,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE
    #     )
    #     proc1.stdout.close()
    #     out, err = proc2.communicate()

    #     print ("out: {0}", out)
    #     print ("err: {0}", format(err))


    git_tree = subprocess.run(
       [
           "git",
           "ls-tree",
           "-r",
           "--name-only",
           default_branch
       ],
       capture_output=True,
       check=True,
       text=True,
       cwd=f"{GIT_CLONE_PATH}"
    )
    out_files_repo = git_tree.stdout
    #print (out_files_repo)

    for manifest_name in manifest_count_dict:
        # number_manifest = out_files_repo.count(manifest_name)
        # print("type : ", manifest_name, " number: ", number_manifest)
        manifest_count_dict[manifest_name]= out_files_repo.count(manifest_name)
    
    for manifest_file_types,manifest_file_counts in list(manifest_count_dict.items()):
        if manifest_file_counts == 0:
            del manifest_count_dict[manifest_file_types] 


    print(f"  - removing cloned files in /tmp...")
    subprocess.run(["rm", "-fr", f"{GIT_CLONE_PATH}"], check=True)

    return manifest_count_dict


def main(
    giturl: str = typer.Option(None, "--gitrepo", help = "If getting manifest files for a repo, enter the git url with this option"), 
    gitdefaultbranch: str = typer.Argument ("main", envvar="DEFAULT_BRANCH", help="Default branch for the repo, required if getting manifest files within a repo."),
    githuborg: str = typer.Option(None, "--githuborg", help="If getting manifest files for repos within a GitHub org, enter the name of the GitHub Organization with this option."), 
    outputfile: str = typer.Argument("manifestcount.json", help="The name of the json file to output manifest file counts in the root directory."),
    ghtoken: str = typer.Argument (None, envvar="GITHUB_TOKEN", help="Github Personal Access Token, required if getting manifest files within a GitHub Org.",show_default=False)):
    jsonoutputfile = open(outputfile, "w")
    jsonoutputfile.close()
    
    if giturl:
        # print(f"hi {giturl}")
        manifest_count = get_manifest_from_clone(giturl, gitdefaultbranch)
        manifest_count_with_repo = {
                "repo_url": giturl,
                "manifest_files": manifest_count
            }
        serialize_manifest = json.dumps(manifest_count_with_repo,indent=4)
        print (serialize_manifest)
        with open(outputfile,"a") as jsonoutputfile:
            jsonoutputfile.write(serialize_manifest)
            jsonoutputfile.close()
    if githuborg:
        ghrepos = get_repos_given_org(githuborg,ghtoken)
        dict_of_repos = []
        for ghrepo in ghrepos:
            giturl = ghrepo['html_url']
            defaultbranch = ghrepo['default_branch']
            manifest_count = get_manifest_from_clone(giturl, defaultbranch)
            manifest_count_with_repo = {
                "full_repo_name": ghrepo['full_name'],
                "manifest_files": manifest_count
            }
            dict_of_repos.append(manifest_count_with_repo)
        serialize_manifest = json.dumps(dict_of_repos,indent=4)
        print(serialize_manifest)
        with open (outputfile,"a") as jsonoutputfile:
            jsonoutputfile.write(serialize_manifest)
            jsonoutputfile.close()
            
if __name__ == "__main__":
    typer.run(main)
