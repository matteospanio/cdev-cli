"""Common functions for the cdev_cli package."""

import shutil
import subprocess
from enum import Enum

STATUS_MSG = {
    "RUNNING": "",
    "NOT_FOUND": "Docker executable has not been found in your environment.\n"
    "Please install docker or add it to the PATH.",
    "NOT_RESPONDING": "Docker is not responding.",
    "NOT_RUNNING": "Docker is not running.",
}


class DockerStatus(str, Enum):
    """Enum class to represent the status of the docker daemon."""

    RUNNING = "RUNNING"
    NOT_FOUND = "NOT_FOUND"
    NOT_RESPONDING = "NOT_RESPONDING"
    NOT_RUNNING = "NOT_RUNNING"


def get_docker_status() -> DockerStatus:
    """Check the status of the docker daemon.

    Returns
    -------
    DockerStatus
        The status of the docker daemon.

    """
    if not shutil.which("docker"):
        return DockerStatus.NOT_FOUND

    try:
        process = ["docker", "info"]
        subprocess.check_call(
            process,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            timeout=10,
            shell=False,  # noqa: S603
        )
        return DockerStatus.RUNNING
    except subprocess.CalledProcessError:
        return DockerStatus.NOT_RUNNING
    except subprocess.TimeoutExpired:
        return DockerStatus.NOT_RESPONDING
