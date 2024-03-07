from argparse import ArgumentParser, HelpFormatter
from pathlib import Path
import itertools
import os
import subprocess
import sys
from typing import NoReturn

from unipd_cdev import lib
from unipd_cdev.lib import DockerStatus


class CapitalizedHelpFormatter(HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = "Usage: "
        return super(CapitalizedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix
        )


def init_parser(parser: ArgumentParser) -> ArgumentParser:
    parser._positionals.title = "Positional arguments"
    parser._optionals.title = "Optional arguments"
    parser.add_argument(
        "folder",
        default=os.getcwd(),
        nargs="?",
        type=Path,
        help="the folder to mount into the docker container (defaults to $PWD).",
    )
    parser.add_argument(
        "-t",
        "--tag",
        nargs="?",
        help="start matteospanio/corso-c:TAG, else matteospanio/corso-c:latest",
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
    parser = ArgumentParser(
        prog="unipd-cdev",
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
        sys.exit(os.EX_USAGE)

    command = ["docker", "run"]
    options = ["-v", f"{folder}:/mnt/", "-it", "--rm", f"matteospanio/corso-c:{tag}"]
    args = ["bash"]

    process = list(itertools.chain(command, options, args))
    subprocess.run(process)

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
