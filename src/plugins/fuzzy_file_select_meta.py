import os, json

def write_data(dirname, file_data):
    paths = []

    for dirname, dirnames, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if filename not in ['.shimdata']:
                paths.append(os.path.join(dirname, filename))

    for path in paths:
        try:
            file_data['fuzzy_file_select'][os.path.relpath(path, dirname)] = path
        except KeyError:
            file_data['fuzzy_file_select'] = { os.path.relpath(path, dirname): path }


