from aiogram.types import Message, File
from aiogram import Bot
from pathlib import Path

from gpt.gpt import OpenAIAPI
from services.gpt_services import handle_gpt_response
from tasks import delete_handled_file


async def download_file(file: File, file_name: str, path: str, bot: Bot):
    # Ensure the path exists
    Path(path).mkdir(parents=True, exist_ok=True)

    # Download the file
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


async def voice_message_handler(message: Message, bot: Bot) -> None:
    telegram_id = message.chat.id
    message_id = message.message_id
    voice_file = await bot.get_file(message.voice.file_id)
    path = "media/voices"

    await download_file(file=voice_file, file_name=f"{voice_file.file_id}.wav", path=path, bot=bot)

    destination = f"{path}/{voice_file.file_id}.wav"
    with open(destination, "rb") as audio_file:
        openai = OpenAIAPI()
        transcription = openai.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        await handle_gpt_response(telegram_id, [message_id, transcription.text])
    delete_handled_file.delay(destination)
