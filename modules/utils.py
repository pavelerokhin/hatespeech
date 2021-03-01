import sys

import yaml


def open_and_parse_yaml(file_name, error_message):
    conf = ""
    try:
        with open(file_name, "r") as file:
            conf = yaml.load(file, Loader=yaml.FullLoader)
            if not conf:
                print(error_message)
                sys.exit(1)
    except FileNotFoundError:
        print("file", file_name, "does not exist")
        sys.exit(1)

    return conf