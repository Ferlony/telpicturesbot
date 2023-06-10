import json
import xxhash
from os import path, walk, sep, mkdir
from shutil import rmtree, copy


def get_files_in_dir(directory):
    files_list = []
    counter = 0
    for root, dirs, files in walk(directory):
        for filename in files:
            files_list.append(filename)
            counter += 1
    return files_list, counter


def get_file_types_in_list(some_list):
    file_extensions = []
    for i in range(0, len(some_list)):
        file_name, file_extension = path.splitext(some_list[i])
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


def file_checker(file):
    json_file_location = "local" + sep + "allowed_formats.json"

    with open(json_file_location, "r") as json_file:
        allowed_formats = json.load(json_file)

    file_name, file_extension = path.splitext(file)

    for key, types in allowed_formats.items():
        if file_extension in types:
            return key

    return None


def create_folder(new_dir, file_location_path, renamed_files_folder):
    try:
        mkdir(new_dir)
    except:
        try:
            mkdir(file_location_path + renamed_files_folder)
            mkdir(new_dir)
        except:
            rmtree(new_dir)
            mkdir(new_dir)
    return


def get_folder_name(folder):  # TODO delete it
    if folder[-1] == sep:
        string_name = ""
        i = -1
        while True:
            i -= 1
            if folder[i] == sep:
                string_name = sep + str(string_name[::-1])
                return string_name
            string_name += folder[i]
    else:
        return sep + "SomeFileName"


def rename_one_file_by_hash(picture_location, file):
    file_location_path = path.dirname(__file__)
    dir_name = get_folder_name(picture_location + sep)  # TODO change it
    renamed_files_folder = sep + "local" + sep + "pictures" + sep + "sentfiles"
    new_dir = file_location_path + renamed_files_folder + dir_name

    create_folder(new_dir, file_location_path, renamed_files_folder)

    file_name, file_extension = path.splitext(file)
    file_hash = xxhash.xxh3_128_hexdigest(file_name)

    renamed_file = file_hash + file_extension

    copy(picture_location + sep + file, new_dir + sep + renamed_file)
    return str(new_dir + sep + renamed_file)


def rename_one_file_by_hash_one(file):
    file_location_path = path.dirname(__file__)
    dir_name = "SomeSingleFileByHand"
    renamed_files_folder = sep + "local" + sep + "pictures" + sep + "sentfiles"
    new_dir = file_location_path + renamed_files_folder + dir_name

    create_folder(new_dir, file_location_path, renamed_files_folder)

    file_name, file_extension = path.splitext(file)
    file_hash = xxhash.xxh3_128_hexdigest(file_name)

    renamed_file = file_hash + file_extension

    copy(file, new_dir + sep + renamed_file)
    return str(new_dir + sep + renamed_file)

