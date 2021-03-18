import subprocess
import sys


def install(package, *options, venv=False):
    if venv:
        options = " ".join(options)
        subprocess.check_call(
            f". env/bin/activate && python -m pip install {package} {options} && deactivate",
            shell=True,
        )
    else:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package, *options]
        )


def create_environment():
    import virtualenv

    virtualenv.cli_run(["env", "--system-site-packages"])


def create_docs():
    subprocess.check_call(
        ["sphinx-quickstart", "-q", "-p", "my", "-a", "me", "--sep"], cwd="docs"
    )


def run_tests():
    subprocess.check_call(["pytest"])


if __name__ == "__main__":
    install("virtualenv", "--upgrade")

    create_environment()

    #  install("--editable", ".", venv=True)

    install("--requirement", "doc_requirements.txt", "--ignore-installed", venv=True)
    create_docs()

    install("--requirement", "test_requirements.txt", "--ignore-installed", venv=True)
    #  run_tests()
