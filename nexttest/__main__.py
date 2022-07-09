import argparse
import os
from typing import Optional

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
    choices=[],
    help="Only run tests for this pr",
)
parser.add_argument(
    "--discover",
    type=dir_path,
    help="Discover and run tests in the given directory",
)
args = parser.parse_args()
pr: Optional[str] = args.pr
repo: Optional[str] = args.repo
discover_dir: Optional[str] = args.discover

if (pr or repo) and discover_dir:
    parser.error("Cannot use --discover with --pr or --repo")

elif discover_dir:
    pytest_args: str = f"{discover_dir}"
    pytest.main(pytest_args.split(" "))
