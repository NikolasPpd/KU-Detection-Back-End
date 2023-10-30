import os


def get_file_extension(file_name: str) -> str:
    """Gets the extension of the given file name.

    :param file_name: The name of the file.
    :return: The extension of the given file name."""
    return os.path.splitext(file_name)[1]


def is_file_accepted(file_name: str, accepted_file_types: list) -> bool:
    """Checks whether the given file name has an extension that is in the accepted_file_types list.

    :param file_name: The name of the file.
    :param accepted_file_types: A list of accepted file types.
    :return: True if the given file name has an extension that is in the accepted_file_types list, False otherwise.
    If the accepted_file_types is None, all file types are accepted."""
    if accepted_file_types is None:
        return True
    return get_file_extension(file_name) in accepted_file_types
