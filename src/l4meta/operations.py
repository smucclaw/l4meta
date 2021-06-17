"""Operations."""

import os
import shlex
import l4meta
import l4meta.executable as executable
import l4meta.metadata as mt

from l4meta.errors import ExifToolError
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


def get_config_path(
        directory: str = 'config', resource: str = 'xmp.config') -> str:
    """Get the path of the config file."""
    module_path = os.path.dirname(l4meta.__file__)
    return os.path.join(module_path, directory, resource)


def get_absolute_path(location: str, check_required: bool = True) -> str:
    """Get the absolute path of a file."""
    path = os.path.abspath(location)
    if check_required and not os.path.isfile(path):
        raise ExifToolError(f'File not found - {path}')
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
        raise ExifToolError(f'Not an allowed filetype - {ext[1:]}')


def run(arguments: str) -> CompletedProcess:
    """Execute the command."""
    bin_exiftool = executable.binary('exiftool')
    path_config = get_config_path()

    args_builder = f'{bin_exiftool} -config {path_config} {arguments}'
    args = shlex.split(args_builder, posix=0)
    return executable.execute(args)


def read(filenames: List[str], format: str = 'json') -> str:
    """Read metadata from multiple files."""
    if not filenames:
        raise ExifToolError()
    if len(filenames) == 1:
        metadata = read_single(filenames[0], format)
        return mt.dump(metadata)
    if True:
        read_multiple(filenames, format)


def read_single(filename: str, format: str = 'json') -> str:
    """Read metadata from a single file."""
    filename = get_absolute_path(filename)
    is_allowed_filetype(filename)

    command = f'-j {filename}'
    process = run(command)
    if process.returncode != 0:
        raise ExifToolError('Unable to read file!')

    output = process.stdout
    return mt.convert_to_output(output)


def read_multiple(filenames: List[str], format: str = 'json') -> str:
    """Read metadata from multiple files."""
    for file in filenames:
        filename = get_matching_filename(file)
        metadata = read_single(file, format)
        with open(filename, 'w') as out:
            out.write(metadata)


def write_single(input_file: str, output_file: str, metadata: str) -> bool:
    """Write metadata to a single file."""
    if output_file == '-':
        raise ExifToolError(f'\'-\' not supported yet!')
    input_file = get_absolute_path(input_file)
    output_file = get_absolute_path(output_file, False)
    is_allowed_filetype(input_file)
    is_allowed_filetype(output_file)

    metadata = mt.flatten(metadata)
    process = write_metadata(metadata, input_file, output_file)
    return process.returncode == 0


def write_multiple() -> None:
    pass


def write_metadata(
        metadata: str, input_file: str, output: str = '-',
        temporary_file: str = 'temp_meta.json') -> CompletedProcess:
    """Write metadata for a single input file to a single output."""
    temporary_file = f'{gettempdir()}/{temporary_file}'
    with open(temporary_file, 'w+') as t:
        t.write(metadata + "\n")
    command = f'-j+={temporary_file} -q -o {output} {input_file}'
    process = run(command)

    os.remove(temporary_file)
    return process
