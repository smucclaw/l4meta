"""Functions for running executables."""

import subprocess
import shutil

from subprocess import CompletedProcess
from typing import List
from l4meta.errors import ExifToolError

__all__ = ['binary', 'execute']


def binary(executable: str) -> str:
    """Check that the executable is present."""
    bin_path = shutil.which(executable)
    if not bin_path:
        raise ExifToolError(f'{executable} not installed!')
    return bin_path


def execute(arguments: List[str]) -> CompletedProcess:
    """Execute the command."""
    return subprocess.run(
        arguments,
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
