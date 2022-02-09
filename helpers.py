import os
import sys
import json


def check_and_fix_dir_path(dir_path):
    if dir_path[-1] != '/':
        dir_path += '/'

    return dir_path


def check_and_fix_file_extension(filename, expected_extension):
    if expected_extension[0] == '.':
        expected_extension = expected_extension[1:]

    ext_length = len(expected_extension)
    assert ext_length > 0

    if filename[-ext_length:] != expected_extension:
        return filename + '.' + expected_extension

    return filename


def get_python_version():
    return "python" + str(sys.version_info[0]) + '.' + str(sys.version_info[1])


def read_json_file_to_dict(json_filename):
    with open(json_filename) as f:
        json_dict = json.load(f)

    return json_dict


# Write json_dict object to json file
def write_dict_to_json_file(json_dict, filename):

    with open(filename + '.json', 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

    json_file.close()


def makedir(parent_dir, dir_name):
    directory = os.path.join(parent_dir, dir_name)
    if not os.path.isdir(directory):
        os.mkdir(directory)
