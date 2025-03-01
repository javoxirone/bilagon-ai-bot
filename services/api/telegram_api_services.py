from aiogram.types import voice

from utils.api.telegram_api_utils import download_file


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
