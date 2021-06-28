"""Operations."""

import os
import shlex
import l4meta
import l4meta.executable as executable
import l4meta.metadata as mt

from subprocess import CompletedProcess
from tempfile import gettempdir
from typing import List

__all__ = [
        'read',
        'read_single',
        'read_multiple',
        'write_single',
        'write_multiple'
]


def get_config_path(location: str = 'config/xmp.config') -> str:
    """Get the path of the config file."""
    module_path = os.path.dirname(l4meta.__file__)
    return os.path.join(module_path, location)


def get_absolute_path(location: str, check_required: bool = True) -> str:
    """Get the absolute path of a file."""
    path = os.path.abspath(location)
    if check_required and not os.path.isfile(path):
        raise FileNotFoundError(f'File not found - {path}')
    return path


def get_matching_filename(filename: str, format: str = 'json') -> str:
    """Get the new filename of the file that matches the original filename."""
    name, _ = os.path.splitext(filename)
    return f'{name}.yml' if format == 'yaml' else f'{name}.json'


def is_allowed_filetype(
        location: str, allowed_filetypes: List[str] = ['pdf']) -> None:
    """Check that the file is among the approved filetypes."""
    _, ext = os.path.splitext(location)
    if ext[1:] not in allowed_filetypes:
        raise Exception(f'Not an allowed filetype - {ext[1:]}')


def run(arguments: str) -> CompletedProcess:
    """Execute the command."""
    bin_exiftool = executable.binary('exiftool')
    path_config = get_config_path()

    args_builder = f'{bin_exiftool} -config {path_config} {arguments}'
    args = shlex.split(args_builder, posix=0)
    return executable.execute(*args)


def read(filenames: List[str], format: str = 'json') -> str:
    """Read metadata from multiple files."""
    if not filenames:
        raise Exception('No files read!')
    if len(filenames) == 1:
        return read_single(filenames[0], format)
    if True:
        read_multiple(filenames, format)
        return 'Successfully written metadata!'


def read_single(filename: str, format: str = 'json') -> str:
    """Read metadata from a single file."""
    filename = get_absolute_path(filename)
    is_allowed_filetype(filename)

    command = f'-j {filename}'
    process = run(command)
    if process.returncode != 0:
        raise Exception('Unable to read file!')

    output = process.stdout
    metadata = mt.convert_to_output(output)
    return mt.dump(metadata, format)


def read_multiple(filenames: List[str], format: str = 'json') -> None:
    """Read metadata from multiple files."""
    for file in filenames:
        filename = get_matching_filename(file, format)
        metadata = read_single(file, format)
        mt.write_file(filename, metadata)


def write_single(input_file: str, output_file: str, metadata: str) -> bool:
    """Write metadata to a single file."""
    if output_file == '-':
        raise Exception('\'-\' not supported yet!')
    input_file = get_absolute_path(input_file)
    output_file = get_absolute_path(output_file, False)
    is_allowed_filetype(input_file)
    is_allowed_filetype(output_file)

    metadata = mt.flatten(metadata)
    with TemporaryFile(name='temp.json') as temp_file:
        temp_file.write(metadata + "\n")

        command = f'-j+={temp_file.path} -q -o {output_file} {input_file}'
        process = run(command)
        return process.returncode == 0


def write_multiple() -> None:
    """Write metadata for multiple files."""
    pass


class TemporaryFile:
    """Temporary file context manager."""

    def __init__(self, name: str, mode: str = 'w+') -> None:
        self.path = self.get_absolute_path(name)
        self.mode = mode

    def __enter__(self):
        self.file = open(self.path, self.mode)
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.file.close()
        os.remove(self.path)
        return self

    def get_absolute_path(self, location: str) -> str:
        """Get the absolute path of the file."""
        return os.path.join(gettempdir(), location)

    def write(self, contents: str) -> None:
        """Write the file."""
        self.file.write(contents)
        self.file.seek(0)
