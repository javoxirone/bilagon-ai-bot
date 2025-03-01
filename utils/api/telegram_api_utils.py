import os
from config.integrations import bot


async def download_file(file_obj: object, dir_path: str, file_name: str, file_type: str) -> str:
    """
    This utility function downloads the file according to the passed parameters.

    :param file_obj: The telegram file object (e.g. voice, photo, etc.).
    :type file_obj: object

    :param dir_path: Path to the directory where the file is to be downloaded.
    :type dir_path: str

    :param file_name: The name of the file to be downloaded.
    :type file_name: str

    :param file_type: The type of file to be downloaded.
    :type file_type: str

    :return: The full path of the downloaded file.
    :rtype: str
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        path = f"{dir_path}/{file_name}.{file_type}"
        await bot.download(file_obj, destination=path)
        return path
    except FileExistsError:
        raise FileExistsError("File already exists")
    except Exception as e:
        raise e