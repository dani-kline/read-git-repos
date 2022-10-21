MANIFEST_PATTERN_SCA = '^(?![.]).*(package[.]json|Gemfile[.]lock|pom[.]xml|build[.]gradle|.*[.]lockfile|build[.]sbt|.*req.*[.]txt|Gopkg[.]lock|go[.]mod|vendor[.]json|packages[.]config|.*[.]csproj|.*[.]fsproj|.*[.]vbproj|project[.]json|project[.]assets[.]json|composer[.]lock|Podfile|Podfile[.]lock)$'

def get_git_tree_from_clone(repo_name, origin):
    """
    get git tree for large repos by performing
    a shallow clone 'git clone --depth 1'
    """

    tree_full_paths = []

    gh_client = get_github_client(origin)
    gh_repo = get_github_repo(gh_client, repo_name)

    # check if git exists on the system
    subprocess.run(["command", "-v", "git"], check=True, stdout=subprocess.DEVNULL)

    name = gh_repo.name
    clone_url = gh_repo.clone_url
    default_branch = gh_repo.default_branch

    GIT_CLONE_PATH = f"{common.GIT_CLONE_TEMP_DIR}/{name}"

    # check that GIT_CLONE_PATH is set safely for deletion
    if re.match(f'{common.GIT_CLONE_TEMP_DIR}/.+', GIT_CLONE_PATH) and \
        re.match(rf'\/.+\/.+', GIT_CLONE_PATH):
        pass
    else:
        sys.exit(f"could not determine that the temp cloning directory"
                 f"{GIT_CLONE_PATH} was set properly, exiting...")

    print(f"  - shallow cloning {name} from {clone_url} to {GIT_CLONE_PATH}")

    # clone the repo locally
    subprocess.run(["rm", "-fr", f"{GIT_CLONE_PATH}"], check=True)
    subprocess.run(
        ["git", "clone", "--depth", "1", clone_url],
        check=True,
        cwd=common.GIT_CLONE_TEMP_DIR
    )

    print("  - Loading tree from local git structure")

    git_tree = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            default_branch
        ],
        capture_output=True,
        check=True,
        text=True,
        cwd=f"{GIT_CLONE_PATH}"
    )

    print(f"  - removing cloned files in /tmp...")
    subprocess.run(["rm", "-fr", f"{GIT_CLONE_PATH}"], check=True)

    git_tree_lines = git_tree.stdout.splitlines()
    print(f"  - found {len(git_tree_lines)} tree items ...")

    for line in git_tree_lines:
        sha, path = [line.split()[i] for i in (2, 3)]
        tree_full_paths.append({
            "sha": sha,
            "path": path
        })

    return tree_full_paths
