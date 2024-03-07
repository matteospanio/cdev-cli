"""Entrypoint module, in case you use `python -m cdev_cli`."""

import itertools
import os
import subprocess
import sys
from argparse import ArgumentParser, HelpFormatter
from pathlib import Path
from typing import NoReturn

from cdev_cli import lib
from cdev_cli.lib import DockerStatus


class CapitalizedHelpFormatter(HelpFormatter):
    """Formatter to capitalize the help section titles."""

    def add_usage(self, usage, actions, groups, prefix=None):
        """Override the default usage formatter to capitalize the prefix."""
        if prefix is None:
            prefix = "Usage: "
        return super().add_usage(
            usage,
            actions,
            groups,
            prefix,
        )


def init_parser(parser: ArgumentParser) -> ArgumentParser:
    """Initialize the parser with the required arguments.

    Parameters
    ----------
    parser : ArgumentParser
        The parser to initialize.

    Returns
    -------
    ArgumentParser
        The initialized parser.

    """
    parser._positionals.title = "Positional arguments"
    parser._optionals.title = "Optional arguments"
    parser.add_argument(
        "folder",
        default=Path.cwd(),
        nargs="?",
        type=Path,
        help="the folder to mount into the docker container (defaults to $PWD).",
    )
    parser.add_argument(
        "-t",
        "--tag",
        nargs="?",
        help="start matteospanio/cdev:TAG, else matteospanio/cdev:latest",
        default="latest",
    )
    parser.add_argument(
        "-V",
        "--version",
        version="%(prog)s 0.1.0",
        action="version",
        help="show the version of the program.",
    )
    return parser


def main() -> NoReturn:
    """Entrypoint of the program."""
    parser = ArgumentParser(
        prog="cdev-cli",
        description="CLI interface to run a C development environment through docker.",
        formatter_class=CapitalizedHelpFormatter,
        epilog="This program is distributed under the MIT License.",
    )
    parser = init_parser(parser)
    args = parser.parse_args()

    docker_status = lib.get_docker_status()
    print(lib.STATUS_MSG[docker_status])
    if docker_status != DockerStatus.RUNNING:
        sys.exit(os.EX_UNAVAILABLE if sys.platform != "win32" else 1)

    folder: Path = args.folder
    tag: str = args.tag

    if not folder.exists() or not folder.is_dir():
        print(f"{folder} does not exist or is not a folder.")
        sys.exit(os.EX_USAGE if sys.platform != "win32" else 1)

    command = ["docker", "run"]
    options = ["-v", f"{folder}:/mnt/", "-it", "--rm", f"matteospanio/cdev:{tag}"]
    args = ["bash"]

    process = list(itertools.chain(command, options, args))

    try:
        subprocess.check_call(process, shell=False)  # noqa: S603
    except subprocess.CalledProcessError:
        print("An error occurred while running the docker container.")
        sys.exit(os.EX_UNAVAILABLE if sys.platform != "win32" else 1)

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
