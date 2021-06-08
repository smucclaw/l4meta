"""Find duplicates."""

import os
import stat
import sys
import hashlib


def find_duplicates(directory):
    """Find duplicates in directory."""
    # Dups in format {hash:[names]}
    duplicates = {}
    for dir_name, _, filenames in os.walk(directory):
        print('Scanning %s...' % dir_name)
        for filename in filenames:
            # Get the path to the file
            path = os.path.join(dir_name, filename)
            file_hash = calculate_hash(path)
            # Add or append the file path
            if file_hash in duplicates:
                duplicates[file_hash]['path'].append(path)
            else:
                duplicates[file_hash] = {}
                duplicates[file_hash]['path'] = [path]
                if os.path.isfile(path):
                    duplicates[file_hash]['size'] = os.stat(path)[stat.ST_SIZE]
    return duplicates
 

def join_dictionaries(dict1, dict2):
    """Join two dictionaries."""
    for key in dict2.keys():
        dict1[key] = dict1[key] if key in dict1 else '' + dict2[key]


def calculate_hash(path, blocksize: int = 65536):
    """Calculate hash of a path."""
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def size_format(num, suffix):
    """Format size."""
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def print_results(dict1):
    """Print results."""
    results = list(filter(lambda x: len(x['path']) > 1, dict1.values()))
    summ = 0
    if len(results) == 0:
        print('No duplicate files found.')
        return
    results = sorted(results, key=lambda res: res['size'])
    print('Duplicates:')
    print('___________________')
    for result in results:
        coef = len(result['path']) - 1
        summ += result['size'] * coef
        print('\t%s' % size_format(result['size'], 'B'))
        for subresult in result['path']:
            print('\t\t%s' % subresult)
        print('___________________')
    print('TOTAL SIZE %s' % size_format(summ, 'B'))


if __name__ == '__main__':
    if len(sys.argv) <= 0:
        print('usage: python duplicates.py directory [directory ...]')
    duplicates = {}
    directories = sys.argv[1:]
    for directory in directories:
        # Iterate the folders given
        if not os.path.exists(directory):
            print('%s is not a valid path, please verify' % directory)
            sys.exit()
        # Find the duplicated files and append them to the duplicates
        join_dictionaries(duplicates, find_duplicates(directory))
    print_results(duplicates)
