import os, re, json
import time

IGNORELIST=['.shimdata']

def get_abpaths():
    paths = []
    for dirname, dirnames, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if filename not in IGNORELIST:
                paths.append(os.path.join(dirname, filename))
    return paths


def create_metadata_files():
    paths = get_abpaths()
    for dirname, dirnames, filenames in os.walk(os.getcwd()):
        table = {}
        for path in paths:
            try:
                table['fuzzy_file_select'][os.path.relpath(path, dirname)] = path
            except KeyError:
                table['fuzzy_file_select'] = { os.path.relpath(path, dirname): path }
        with open(os.path.join(dirname, '.shimdata'), 'w') as f:
            f.write(json.dumps(table))

create_metadata_files()
