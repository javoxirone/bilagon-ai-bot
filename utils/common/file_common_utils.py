def extract_extension(file_name: str) -> str:
    """
    Extract the file extension from a filename.

    :param file_name: The full name of the file.
    :type file_name: str
    :return: The file extension.
    :rtype: str
    """
    import os
    _, extension = os.path.splitext(file_name)

    # Remove the dot from the extension
    if extension and extension[0] == '.':
        extension = extension[1:]

    return extension
