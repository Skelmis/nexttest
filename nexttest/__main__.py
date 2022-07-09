import argparse
import os
from typing import Optional, Dict, List

import pytest


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise parser.error("--discover was not a directory")


parser = argparse.ArgumentParser(description="Run your tests", prog="NextTest")
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
args = parser.parse_args()
pr: Optional[int] = args.pr
repo: Optional[str] = args.repo
discover_dir: Optional[str] = args.discover

if (pr or repo) and discover_dir:
    parser.error("Cannot use --discover with --pr or --repo")

elif discover_dir:
    pytest_args: str = f"{discover_dir}"
    pytest.main(pytest_args.split(" "))

elif repo and not pr:
    path = os.path.join(os.path.dirname(__file__), f"test_{repo}")
    pytest_args: str = f"{path}"
    pytest.main(pytest_args.split(" "))

elif pr and not repo:
    parser.error("--repo is required when using --pr")

elif repo and pr:
    # {Repo: {PR: [test_files]}}
    repo_mappings: Dict[str, Dict[int, List[str]]] = {"nextcord": {}}
    pr_mapping: Dict[int, List[str]] = repo_mappings[repo]
    try:
        pr_test_paths = pr_mapping[pr]
    except KeyError:
        parser.error(f"No pr for {repo} with number {pr}")

    pytest_args: List[str] = []
    for test_path in pr_test_paths:  # noqa # parser.error exists the program
        path = os.path.join(os.path.dirname(__file__), f"test_{repo}", test_path)
        pytest_args.append(path)

    pytest.main(pytest_args)

else:
    parser.print_help()
