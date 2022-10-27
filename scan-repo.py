
from asyncio.subprocess import PIPE
import subprocess
import re
import typer

MANIFEST_PATTERN_SCA = '^(?![.]).*(package[.]json|Gemfile[.]lock|pom[.]xml|build[.]gradle|.*[.]lockfile|build[.]sbt|.*req.*[.]txt|Gopkg[.]lock|go[.]mod|vendor[.]json|packages[.]config|.*[.]csproj|.*[.]fsproj|.*[.]vbproj|project[.]json|project[.]assets[.]json|composer[.]lock|Podfile|Podfile[.]lock)$'
manifest_count_dict = {
    "package.json": 0,
    "pom.xml": 0
}

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

    #git_tree_lines = git_tree.stdout.splitlines()
    #print(f"  - found {len(git_tree_lines)} tree items ...")

    #for line in git_tree_lines:
    #    sha, path = [line.split()[i] for i in (2, 3)]
    #    tree_full_paths.append({
    #        "sha": sha,
    #        "path": path
    #    })

    return manifest_count_dict


# def main(gitrepo: str):
#     print(f"Hello {name}")

def main(giturl: str = typer.Option(..., "--gitrepo")):
    print(f"hi {giturl}")
    manifest_count = get_manifest_from_clone(giturl, "master")
    for manifest_name in manifest_count:
        print("type : ", manifest_name, " number: ", manifest_count[manifest_name])



if __name__ == "__main__":
    typer.run(main)

