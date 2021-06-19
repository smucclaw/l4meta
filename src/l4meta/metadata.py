"""Functions to read and parse metadata."""

import json
import yaml

from l4meta.errors import ExifToolError
from typing import TextIO, List

__all__ = [
        'flatten',
        'dump',
        'parse',
        'write_file',
        'convert_to_output',
        'convert_to_input'
]


def is_allowed_format(
        format: str, allowed_formats: List[str] = ['json', 'yaml']) -> None:
    """Check that the format is among the allowed format."""
    if format not in allowed_formats:
        raise ExifToolError(f'Not an allowed format - {format}')


def is_json(metadata: str) -> bool:
    """Check whether the string is a json."""
    return metadata[0] in ['{', '[']


def read_content(content: TextIO) -> str:
    """Read the metadata file."""
    if content.isatty():
        raise ExifToolError('Need an input to metadata!')
    return content.read()


def write_file(filename: str, content: str) -> None:
    """Write contents of metadata to a file."""
    with open(filename, 'w') as out:
        out.write(content)


def flatten(content: TextIO) -> str:
    """Flatten the metadata."""
    raw_metadata = read_content(content)
    parsed_metadata = parse(raw_metadata)
    return convert_to_input(parsed_metadata)


def dump(meta: dict, format: str = 'json', indent: int = 4) -> str:
    """Convert the metadata into a string depending on the output format."""
    is_allowed_format(format, ['json', 'yaml'])
    if format == 'yaml':
        return yaml.dump(meta)
    return json.dumps(meta, indent=indent)


def parse(metadata: str, is_json=is_json) -> dict:
    """Parse the input string.

    Args:
        metadata
        is_json
    Returns:
        A dict of the metadata which has been parsed
    """
    metadata = metadata.strip()
    if is_json(metadata):
        return json.loads(metadata)
    return yaml.safe_load(metadata)


def convert_to_output(meta: str, prefix: str = 'L4') -> dict:
    """Convert the stringified metadata into metadata in JSON.

    Args:
        meta: The stringified metadata
    Returns:
        A dict of metadata
    """
    try:
        meta = json.loads(meta)
        meta = meta[0][prefix]
        return json.loads(meta)
    except Exception:
        return {}


def convert_to_input(meta: str, prefix: str = 'L4') -> str:
    """Convert the metadata in JSON into stringified metadata.

    Args:
        meta: The metadata in dict
    """
    try:
        meta = json.dumps(meta)
        meta = {prefix: meta}
        return json.dumps(meta)
    except Exception:
        return {}
