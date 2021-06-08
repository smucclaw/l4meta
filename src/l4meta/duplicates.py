"""Find duplicates"""

import stat
import hashlib


def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash]['path'].append(path)
            else:
                dups[file_hash] = {}
                dups[file_hash]['path'] = [path]
                if os.path.isfile(path):
                    dups[file_hash]['size'] = os.stat(path)[stat.ST_SIZE]
    return dups


# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def sizeof_fmt(num, suffix):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def printResults(dict1):
    results = list(filter(lambda x: len(x['path']) > 1, dict1.values()))
    summ = 0
    if len(results) > 0:
        results = sorted(results, key=lambda res: res['size'])
        print('Duplicates:')
        print('___________________')
        for result in results:
            coef = len(result['path']) - 1
            summ += result['size'] * coef
            print('\t%s' % sizeof_fmt(result['size'], 'B'))
            for subresult in result['path']:
                print('\t\t%s' % subresult)
            print('___________________')
        print('TOTAL SIZE %s' % sizeof_fmt(summ, 'B'))

    else:
        print('No duplicate files found.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dups = {}  
        folders = sys.argv[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDicts(dups, findDup(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        printResults(dups)
    else:
        print('Usage: python duplicates_finder.py folder or python duplicates_finder.py folder1 folder2 folder3')    
