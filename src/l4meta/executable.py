"""Functions for running executables."""

import subprocess
import shutil

from subprocess import CompletedProcess

__all__ = ['binary', 'execute']


def binary(executable: str) -> str:
    """Check that the executable is present."""
    bin_path = shutil.which(executable)
    if not bin_path:
        raise Exception(f'{executable} not installed!')
    return bin_path


def execute(*arguments: str) -> CompletedProcess:
    """Execute the command."""
    return subprocess.run(
        arguments,
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
