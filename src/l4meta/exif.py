"""exif.py."""

import subprocess
import os
import shutil

from contextlib import contextmanager
from subprocess import CompletedProcess
from typing import List

__all__ = [
        'ExifTool',
        'ExifToolError'
]


class ExifTool:
    """ExifTool class."""
    BIN_EXIF = 'exiftool'

    def __init__(
            self,
            executable: str = BIN_EXIF) -> None:
        """Initialise the class."""
        self.executable = self.check_bin_present(executable)

    def __repr__(self) -> str:
        """Representation of the class."""
        type_name = type(self).__name__
        arg_strings = []
        star_args = {}
        for arg in self._get_args():
            arg_strings.append(repr(arg))
        for name, value in self._get_kwargs():
            if name.isidentifier():
                arg_strings.append('%s=%r' % (name, value))
            else:
                star_args[name] = value
        if star_args:
            arg_strings.append('**%s' % repr(star_args))
        return '%s(%s)' % (type_name, ', '.join(arg_strings))

    def _get_kwargs(self) -> list:
        return list(self.__dict__.items())

    def _get_args(self) -> list:
        return []

    def check_bin_present(
            self,
            executable: str) -> str:
        """Check that the executable is present."""
        bin_path = shutil.which(executable)
        self.exit_on_error(
                not bin_path,
                """exiftool not installed!
                To install exiftool, run
                sudo apt-get install exiftool""")
        return bin_path

    def execute(
            self,
            args: List[str]) -> CompletedProcess:
        """Execute the command."""
        return subprocess.run(
            [self.executable] + args,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

    def exit_on_error(
            self,
            condition: bool = False,
            message: str = '') -> None:
        """Cause an error to be raised when a condition is met."""
        if condition:
            raise ExifToolError('Error: ' + message)

    @contextmanager
    def cd(
            self,
            new_dir: str,
            previous_dir: str = os.getcwd()) -> None:
        """Change directory."""
        os.chdir(os.path.expanduser(new_dir))
        try:
            yield
        finally:
            os.chdir(previous_dir)


class ExifToolError(Exception):
    """Class for handling errors from ExifTool."""
    pass
