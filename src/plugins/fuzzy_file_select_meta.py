import os, json

def write_data(dirname, file_data, dir_info):
    paths = []

    for dname, _, filenames in dir_info:
        for filename in filenames:
            if filename not in ['.shimdata']:
                paths.append(os.path.join(dname, filename))

    for path in paths:
        try:
            file_data['fuzzy_file_select'][os.path.relpath(path, dirname)] = path
        except KeyError:
            file_data['fuzzy_file_select'] = { os.path.relpath(path, dirname): path }
