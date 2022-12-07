
from asyncio.subprocess import PIPE
import subprocess
import re
import json
import typer
import requests

MANIFEST_PATTERN_SCA = '^(?![.]).*(package[.]json|Gemfile[.]lock|pom[.]xml|build[.]gradle|.*[.]lockfile|build[.]sbt|.*req.*[.]txt|Gopkg[.]lock|go[.]mod|vendor[.]json|packages[.]config|.*[.]csproj|.*[.]fsproj|.*[.]vbproj|project[.]json|project[.]assets[.]json|composer[.]lock|Podfile|Podfile[.]lock)$'
manifest_count_dict = {
    "package.json": 0,
    "pom.xml": 0
}

def get_repos_given_org(git_org, ghtoken):
    """
    Uses GH API to get list of repos for get_manifest_from_clone
    """
    getreposurl = 'https://api.github.com/orgs/'+{git_org}+'/repos'
    getreposheader = {'Authorization': 'token' + ghtoken }
    ghrepos = requests.get(getreposurl, headers=getreposheader)
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


    print(f"  - removing cloned files in /tmp...")
    subprocess.run(["rm", "-fr", f"{GIT_CLONE_PATH}"], check=True)

    return manifest_count_dict


def main(giturl: str = typer.Option("--gitrepo", help = "If getting manifest files for a repo, enter the git url with this option"), gitorg: str = typer.Option("--gitorg", help="If getting manifest files for repos within a GitHub org, enter the name of your GitHub Organization with this option."), ghtoken: str = typer.Argument (None, envvar="GITHUB_TOKEN", help="Github Personal Access Token, required if getting manifest files withing a GitHub Org. Accepts GITHUB_TOKEN as an environmental variable.")):
    # if --gitorg isn't entered, is gitorg undefined or is it ""
    # Also, is this necessary? Unsure if this is suficcient or will create issues later on w/ none or both inputs
    # gh -- optional argument with none as default variable? Optional isn't working so unsure. Also unsure how to document the env variable required--token.
    if giturl:
        print(f"hi {giturl}")
        manifest_count = get_manifest_from_clone(giturl, "master")
        serialize_manifest = json.dumps(manifest_count)
        print (serialize_manifest)
    if gitorg:
        ghrepos = get_repos_given_org(gitorg,ghtoken)
        for ghrepo in ghrepos:
            ghrepourl = ghrepo['owner']['url']
            manifest_count = get_manifest_from_clone(ghrepourl, "master")
            serialize_manifest = json.dumps(manifest_count)
            print(f"hi {ghrepourl}")



if __name__ == "__main__":
    typer.run(main)

