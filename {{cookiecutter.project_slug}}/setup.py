# -*- coding: utf-8 -*-
import pathlib

import packutil as pack
from setuptools import setup, find_packages

MAJOR = 0
MINOR = 0
MICRO = 1

repo_path = pathlib.Path(__file__).absolute().parent


{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

def setup_package():
    # write version
    pack.versions.write_version_py(
        MAJOR,
        MINOR,
        MICRO,
        pack.versions.is_released(repo_path),
        filename="src/{{ cookiecutter.project_slug }}/version.py",
    )
    # paste Readme
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # do it
    setup(
        name="{{ cookiecutter.project_slug }}",
        version=pack.versions.mkversion(MAJOR, MINOR, MICRO),
        description="{{ cookiecutter.project_short_description }}",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
        author_email="{{ cookiecutter.email }}",
        url="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}",
        package_dir={"": "src"},
        packages=find_packages("src"),
        package_data={"{{ cookiecutter.project_slug }}": []},
        zip_safe=False,
        classifiers=[
{%- if cookiecutter.open_source_license in license_classifiers %}
            "{{ license_classifiers[cookiecutter.open_source_license] }}",
{%- endif %}
            "Natural Language :: English",
            "Programming Language :: Python :: 3",
        ],
        install_requires=[],
        python_requires=">=3.7",
    )


if __name__ == "__main__":
    setup_package()
