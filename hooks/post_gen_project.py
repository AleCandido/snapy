import subprocess
import sys


def install(package, *options, venv=False):
    if venv:
        options = " ".join(options)
        subprocess.check_call(
            " && ".join(
                [
                    ". env/bin/activate",
                    f"python -m pip install {package} {options}",
                    "deactivate",
                ]
            ),
            shell=True,
        )
    else:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package, *options]
        )


def create_environment():
    import virtualenv

    virtualenv.cli_run(["env", "--system-site-packages"])


def create_repo():
    import pygit2

    # create first commit
    repo = pygit2.init_repository(".")
    repo.index.add_all()
    user = repo.default_signature
    tree = repo.index.write_tree()
    parent = []
    commit = repo.create_commit(
        "HEAD", user, user, "Init {{ cookiecutter.project_slug }}", tree, parent
    )
    repo.index.write()

    # create first tag
    repo.create_tag(
        "v0.0.1",
        commit.hex,
        pygit2.GIT_OBJ_COMMIT,
        repo[commit].author,
        repo[commit].message,
    )


def create_docs():
    subprocess.check_call(
        " && ".join(
            [
                ". ../env/bin/activate",
                "sphinx-quickstart --quiet --project {{ cookiecutter.project_slug }} --author '{{ cookiecutter.full_name }}' --sep",
                "deactivate",
            ]
        ),
        cwd="docs",
        shell=True,
    )


def run_tests():
    subprocess.check_call(
        " && ".join([". env/bin/activate", "pytest", "deactivate"]), shell=True
    )


if __name__ == "__main__":
    install("virtualenv", "--upgrade")

    create_environment()

    install("pygit2", "--upgrade", venv=True)
    create_repo()
    install("--editable", ".", venv=True)

    install("--requirement", "doc_requirements.txt", "--ignore-installed", venv=True)
    create_docs()

    install("--requirement", "test_requirements.txt", "--ignore-installed", venv=True)
    run_tests()
