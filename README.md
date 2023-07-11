# L4 Metadata Tool

The `l4meta` tool is a command line tool to read/write metadata to/from a PDF document.

What document? Perhaps a commercial contract, like a lease or sales agreement.

What metadata? Perhaps an encoding of that contract in a DSL like L4.

This allows "dumb PDFs" to become "smart", by embedding the semantics
of the contract in the contract itself, in a machine-readable way.

## Inspiration

Photographs are JPEGs containing EXIF metadata.

Why aren't contracts PDFs containing L4 metadata?

## Features

- Read/Write metadata directly from/to PDFs
- Specify metadata in `json` and `yaml` formats
- Platform agnostic, can be run on multiple platforms including Windows, macOS and Linux

## Installation

You will need:
- Python 3.6 and above
- [exiftool](https://exiftool.org/)

To install, clone this repository and run:

```sh
pip install .
```

## Usage

```console
usage: l4meta [-h] [--type {json,yaml} | -j | -y] [-w [file ...]] [-m [file]]
              [file ...]

Read/Write L4 metadata

positional arguments:
  file                  location of document

optional arguments:
  -h, --help            show this help message and exit
  --type {json,yaml}    specify metadata output format
  -j, --json            output metadata in JSON, same as --type json
  -y, --yaml            output metadata in YAML, same as --type yaml
  -w [file ...], --write [file ...]
                        location of document to be written
  -m [file], --meta [file]
                        location of metadata
```

## Quick Start

In the `demo/` directory you will find:
- plain.pdf
- greeting.pdf

### Reading

```console
$ l4meta [file ...]
```

#### Single File

For example, to read **greeting.pdf**, execute the following command:

```console
$ l4meta greeting.pdf
```

The output will be the metadata of **greeting.pdf** in **json** format, as below:

```console
{
    "greeting": "Hello World!"
}
```

Adding a `--type yaml`, `--yaml` or `-y` flag like so:

```console
$ l4meta -y greeting.pdf
```

...will cause the output the metadata of the same **greeting.pdf** to be in **yaml**:

```console
greeting: Hello World!

```

However, if you run the same command for **plain.pdf**, it will return:

```console
{ }
```

#### Multiple Files

To read multiple files, execute the following command:

```console
$ l4meta *.pdf
```

In the case of the `demo\` directory, it will output two **json** files: `plain.json` and `greeting.json`.

You can also use the `--type yaml`, `--yaml` or `-y` just as you would for a single file. It will output two **yaml** files: `plain.yml` and `greeting.yml`.

### Writing

```console
$ l4meta file [--write [file ...]] [--meta [file]]
```

For writing, metadata is always written to a duplicate copy of your existing document and never to your original copy. You must specify the location of your original file which you intend to write your metadata, as well as the location of your duplicate file in the `-w` or `--write` flag, which will be the same copy as your original file with metadata written. The original file remains completely untouched; however, any existing metadata that you have in your original copy will be overwritten in your duplicate copy.

When writing metadata to a single file, you must also specify the `-m` or `--meta` flag, which is the location of your metadata.

For example, to write the same metadata in **greeting.pdf** into **plain.pdf**, execute any of the following commands, all of which perform the same function. The metadata will be written into a new **plainv1.pdf**, which is a duplicate of **plain.pdf**, but with metadata.

```console
$ l4meta greeting.pdf > greeting.json
$ l4meta plain.pdf --write plainv1.pdf --meta greeting.json
```

```console
$ l4meta greeting.pdf > greeting.json
$ l4meta plain.pdf --write plainv1.pdf --meta < greeting.json
```

```console
$ l4meta greeting.pdf | l4meta plain.pdf --write plainv1.pdf --meta
```

You can verify that your new **plainv1.pdf** file has the metadata; just follow the instructions from the [Reading](#reading) section above but replace the filename to be read with the location of your new file, e.g. **plainv1.pdf**.
