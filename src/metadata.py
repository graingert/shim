import os, json
# BEGIN code-generated list of module imports
from plugins import fuzzy_file_select_meta
# END code-generated list of module imports

def create_metadata_files():
    for dirname, dirnames, filenames in os.walk(os.getcwd()):
        file_data = {}
        # BEGIN code-generated list of modules to call write_data
        MODULES = [fuzzy_file_select_meta]
        # END code-generated list of modules to call write_data
        for module in MODULES:
            module.write_data(dirname, file_data, os.walk(os.getcwd()))

        with open(os.path.join(dirname, '.shimdata'), 'w') as f:
            f.write(json.dumps(file_data))

create_metadata_files()
