import argparse
import logging
import os
import platform
import subprocess
from typing import Optional, Dict, List, Literal
import importlib

import pytest

log = logging.getLogger(__name__)


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise parser.error("--discover was not a directory")


parser = argparse.ArgumentParser(
    description="Run your tests.\nExtra arguments will be passed directly to pytest",
    prog="NextTest",
)
parser.add_argument(
    "--repo",
    choices=["nextcord", "disnake"],
    help="The repo's tests to run",
)
parser.add_argument(
    "--pr",
    type=int,
    help="Only run tests for this pr",
)
parser.add_argument(
    "--discover",
    type=dir_path,
    help="Discover and run tests in the given directory",
)
args, unknown = parser.parse_known_args()
pr: Optional[int] = args.pr
discover_dir: Optional[str] = args.discover
repo: Optional[Literal["nextcord", "disnake"]] = args.repo


def ensure_package(package: Literal["nextcord", "disnake"]):
    """Ensures the correct package installed"""
    try:
        importlib.import_module(package)
    except ModuleNotFoundError:
        install_link = (
            "https://github.com/DisnakeDev/disnake.git"
            if repo == "disnake"
            else "https://github.com/nextcord/nextcord.git"
        )
        parser.error(
            f"Please make sure to have {package} installed from git, get it with:\n> pip install git+{install_link}"
        )


if (pr or repo) and discover_dir:
    parser.error("Cannot use --discover with --pr or --repo")

elif discover_dir:
    unknown.append(discover_dir)
    pytest.main(unknown)

elif repo and not pr:
    ensure_package(repo)
    path = os.path.join(os.path.dirname(__file__), f"test_{repo}")
    unknown.append(path)
    pytest.main(unknown)

elif pr and not repo:
    parser.error("--repo is required when using --pr")

elif repo and pr:
    ensure_package(repo)
    # {Repo: {PR: [test_files]}}
    # test_files exist in the repo folder
    repo_mappings: Dict[str, Dict[int, List[str]]] = {
        "nextcord": {
            598: ["test_load_extensions"],
            743: ["test_group_mixin_args"],
            706: ["test_remove_view"],
            736: ["test_736"],
            820: ["test_remove_view", "test_remove_modal"],
            812: ["test_812"],
        }
    }
    pr_mapping: Dict[int, List[str]] = repo_mappings[repo]
    try:
        pr_test_paths = pr_mapping[pr]
    except KeyError:
        parser.error(f"No pr for {repo} with number {pr}")

    log.warning(
        "Please make sure the correct branch is installed. Install branches with git+...@branch"
    )

    pytest_args: List[str] = []
    for test_path in pr_test_paths:  # noqa # exists the program
        path = os.path.join(
            os.path.dirname(__file__), f"test_{repo}", f"{test_path}.py"
        )
        pytest_args.append(path)

    pytest_args.extend(unknown)
    pytest.main(pytest_args)

else:
    parser.print_help()
