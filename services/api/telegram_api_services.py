from aiogram.types import voice, document

from utils.api.telegram_api_utils import download_file
from utils.common.file_common_utils import extract_extension


async def download_voice_file(voice_file: voice) -> str:
    try:
        full_path = await download_file(file_obj=voice_file,
                                        dir_path="media/voices",
                                        file_name=voice_file.file_id,
                                        file_type="ogg")
        return full_path
    except FileExistsError as e:
        raise
    except Exception as e:
        raise


async def download_document_file(document_file: document) -> str:
    try:
        full_path = await download_file(file_obj=document_file, dir_path="media/documents",
                                        file_name=document_file.file_id, file_type=extract_extension(document_file.file_name))
        return full_path
    except FileExistsError as e:
        raise
    except Exception as e:
        raise
