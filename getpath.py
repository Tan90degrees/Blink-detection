import os


def get_3rd_path(name1, name2) -> str:
    pwd = os.getcwd()
    path_2rd = os.path.join(pwd, name1)
    path_3rd = os.path.join(path_2rd, name2)
    return path_3rd


def get_2rd_path(name) -> str:
    pwd = os.getcwd()
    path_2rd = os.path.join(pwd, name)
    return path_2rd
