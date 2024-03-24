import os
from .code_file import CodeFile


def read_files_from_directory(directory: str):
    """
    Read the contents of all .java files in the specified directory.

    Parameters:
        directory (str): The directory containing the .java files.

    Returns:
        dict: A dictionary with filenames as keys and their JavaFile objects as values.
    """
    files = [f for f in os.listdir(directory) if f.endswith(".java")]
    contents = {}

    for filename in files:
        file_path = os.path.join(directory, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            contents[filename] = CodeFile(filename, f.read())

    return contents


def read_files_from_dict_list(dict_list: list):
    """
    Read the contents of all .java files in the specified directory.

    Parameters:
        dict_list (list): A list of git contribution dictionaries.

    Returns:
        dict: A dictionary with filenames as keys and their JavaFile objects as values.
    """
    contents = {}

    for contribution in dict_list:
        filename = os.path.basename(contribution["temp_filepath"]).split(".")[0]
        contents[filename] = CodeFile(filename, contribution["file_content"], author=contribution["author"],
                                      timestamp=contribution["timestamp"])

    return contents
