from typing import Dict
from zipfile import ZipFile


def get_archive_directory_structure(archive: ZipFile) -> Dict:
    """Parses a ZipFile's list of files into a hierarchical representation.
    We need to do this because ZipFile just gives us a list of all files in
    contains and doesn't provide any methods to check which files lie in a
    specific subdirectory.
    Args:
        archive: The archive to parse.
    Returns:
        A nested dictionary. Keys of this dictionary are either file names
        which point to their full path in the archive or directory names
        which again point to a nested dictionary that contains their
        contents.
    Example:
        If the archive would contain the following files::
            ['foo.txt',
             'bar/bar.log',
             'bar/baz.out',
             'bar/boogy/text.out']
        This would be transformed into the following hierarchical form::
            {
                'foo.txt': 'foo.txt',
                'bar': {
                    'bar.log': 'bar/bar.log',
                    'baz.out': 'bar/baz.out',
                    'boogy': {
                        'text.out': 'bar/boogy/text.out'
                    }
                }
            }
    """
    result = {}
    for file in archive.namelist():
        # Skip directories in archive.
        if file.endswith('/'):
            continue

        d = result
        path = file.split('/')[1:]  # [1:] to skip top-level directory.
        for p in path[:-1]:  # [:-1] to skip filename
            if p not in d:
                d[p] = {}
            d = d[p]
        d[path[-1]] = file
    return result

if __name__ == '__main__':
    test = get_archive_directory_structure('data/rumoureval-2019-test-data.zip')
    print(test)