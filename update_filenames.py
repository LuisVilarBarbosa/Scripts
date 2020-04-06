# Developed on March 14, 2020.

import argparse
import os
import sys
import time
from collections import OrderedDict
from typing import List

def get_files(paths: List[str], recursive: bool) -> List[str]:
    queue = paths.copy()
    file_paths = []
    while len(queue) > 0:
        current_path = queue.pop(0)
        if os.path.isdir(current_path):
            names = os.listdir(current_path)
            new_paths = [os.path.join(current_path, name) for name in names]
            for new_path in new_paths:
                if os.path.isfile(new_path):
                    file_paths.append(new_path)
                elif recursive:
                    queue.append(new_path)
        else:
            file_paths.append(current_path)
    file_paths.sort()
    return file_paths

def generate_mapping(paths: List[str], description: str, source: str) -> OrderedDict:
    mapping = OrderedDict()
    for path in paths:
        filename, file_extension = os.path.splitext(path)
        directory, old_name = os.path.split(filename)
        date = time.strftime("%Y-%m-%d %Hh%Mm%S %z", time.localtime(os.path.getmtime(path)))
        new_name = f"{date} - {description} - {old_name} - {source}{file_extension}"
        new_path = os.path.join(directory, new_name)
        mapping[path] = new_path
    return mapping

def print_mapping(mapping: dict) -> None:
    for k, v in mapping.items():
        print(f"- {k}")
        print(f"+ {v}")

def assert_no_collision(mapping: dict) -> None:
    collision_found = False
    for path in mapping.values():
        if os.path.exists(path):
            collision_found = True
            print(f"Collision detected: '{path}' already exists.")
    if collision_found:
        quit()

def rename(mapping: dict) -> None:
    for old_name, new_name in mapping.items():
        os.rename(old_name, new_name)

def revert_rename(mapping: dict) -> None:
    for old_name, new_name in mapping.items():
        if os.path.exists(new_name):
            os.rename(new_name, old_name)

def update_filenames(paths: List[str], recursive: bool, description: str, source: str) -> None:
    file_paths = get_files(paths, recursive)
    mapping = generate_mapping(file_paths, description, source)
    print_mapping(mapping)
    assert_no_collision(mapping)
    option = input("Rename all? (y/n) ")
    if option.lower() == "y":
        print("Operation started.")
        try:
            rename(mapping)
        except Exception as e:
            print(f"The following exception occurred: {e}")
            print("Reverting changes.")
            revert_rename(mapping)
        print("Operation completed.")
    else:
        print("Operation cancelled.")

def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser(f'python3 {argv[0]}')
    parser.add_argument('-r', '--recursive', action='store_true', default=False, required=False, help="perform recursion on subfolders")
    parser.add_argument('descriptions', action='store', nargs=1, type=str, help="any description to put on the new filename", metavar='description')
    parser.add_argument('sources', action='store', nargs=1, type=str, help="any string indicating a source (e.g.: a device or application)", metavar='source')
    parser.add_argument('paths', action='store', nargs='+', type=str, help="the relative or absolute path to a file or folder", metavar='path')
    args = parser.parse_args(argv[1:])
    update_filenames(args.paths, args.recursive, args.descriptions[0], args.sources[0])

if __name__ == "__main__":
    main(sys.argv)
