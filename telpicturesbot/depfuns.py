import os
import json
from os import sep


def get_files_in_dir(directory):
    files_list = []
    counter = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            files_list.append(filename)
            counter += 1
    return files_list, counter


def get_file_types_in_list(some_list):
    file_extensions = []
    for i in range(0, len(some_list)):
        file_name, file_extension = os.path.splitext(some_list[i])
        file_extensions.append(file_extension)

    file_extensions_set = set(file_extensions)
    return file_extensions_set


def conformation():
    while True:
        print("Are you sure?\n'1' Yes\n'0' No")
        inp = input()
        if inp == "1":
            return True
        elif inp == "0":
            return False
        else:
            print("Wrong input")


# TODO need to change logic
def file_checker(file):
    json_file_location = "local" + sep + "allowed_formats.json"

    json_file = open(json_file_location, "r")
    allowed_formats = json.load(json_file)
    json_file.close()

    allowed_formats_list_dooble = []

    for key, types in allowed_formats.items():
        print(key)
        allowed_formats_list_dooble.append(types)

    file_name, file_extension = os.path.splitext(file)

    for i in range(0, len(allowed_formats_list_dooble)):
        for j in range(0, len(allowed_formats_list_dooble[i])):
            if file_extension == allowed_formats_list_dooble[i][j]:
                return True

    return False

# TODO filelist for types
def file_list():
    return
