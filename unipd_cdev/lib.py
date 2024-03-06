from enum import Enum
import shutil
import subprocess


STATUS_MSG = {
    "RUNNING": "",
    "NOT_FOUND": "Docker executable has not been found in your environment.\n"
    "Please install docker or add it to the PATH.",
    "NOT_RESPONDING": "Docker is not responding.",
    "NOT_RUNNING": "Docker is not running.",
}


class DockerStatus(str, Enum):
    RUNNING = "RUNNING"
    NOT_FOUND = "NOT_FOUND"
    NOT_RESPONDING = "NOT_RESPONDING"
    NOT_RUNNING = "NOT_RUNNING"


def get_docker_status() -> DockerStatus:
    if not shutil.which("docker"):
        return DockerStatus.NOT_FOUND

    try:
        _ = subprocess.check_call(
            ["docker", "info"],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            timeout=10,
        )
        return DockerStatus.RUNNING
    except subprocess.CalledProcessError:
        return DockerStatus.NOT_RUNNING
    except subprocess.TimeoutExpired:
        return DockerStatus.NOT_RESPONDING
