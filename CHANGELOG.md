# Changelog

## [Unreleased]

## [0.2.0] - 2021-07-01
### Added
- Add batch read functionality ([#3](https://github.com/smucclaw/l4meta/issues/3))
- Add GitHub Actions for flake8 linting on pull request
- Add basic tests for executables

### Changed
- Refactor to use functional paradigm instead of object-oriented, split up code for reusability
- Remove custom exceptions
- `parse_args` in `cli.py` is a separate function
- Update README to include instructions for reading multiple files, remove future work section

## [0.1.2] - 2021-06-10
### Fixed
- Remove code for finding duplicate files due to earlier accidental commit to main branch and subsequent rewrite of git history
- Add repository URL to setup.cfg
- Replace metadata in greeting.pdf with 'hello world'
- Catch Exception rather than Error in cli.py
- Lint with flake8 for exif.py and meta.py
- Update LICENSE to 2021

## [0.1.1] - 2021-06-02
### Added
- Include CHANGELOG file

### Changed
- Refactor `l4meta` package by splitting `exiftool` and `metatool` logic
- Update xmp.config to allow writing to Custom Properties for viewing in Adobe Acrobat
- Repalce greeting.pdf with Custom Properties example
- Exclude all other files except plain.pdf and greeting.pdf in demo directory

## [0.1.0] - 2021-05-31
### Added
- Initial release
