import os
from aiogram.types import Message
from aiogram import Bot
from config.integrations import sr, recognizer
from bot.handlers.message_handlers import handle_gpt_response
from tasks import delete_handled_file

async def voice_message_handler(message: Message, bot: Bot) -> None:
    voice = message.voice
    voice_message_path = os.path.join("media", "voices", f"{voice.file_id}.ogg")
    voice_message_path_output = os.path.join("media", "voices", f"{voice.file_id}.wav")
    await bot.download(voice, destination=voice_message_path)
    ffmpeg_command = f"ffmpeg -i {voice_message_path} {voice_message_path_output}"
    os.system(ffmpeg_command)
    telegram_id = message.from_user.id
    with sr.AudioFile(voice_message_path_output) as source:
        audio_data = recognizer.record(source)

        try:
            # Convert audio to text
            extracted_text = recognizer.recognize_google(audio_data)
            await handle_gpt_response(telegram_id, [message.message_id, extracted_text])
            print("The text from the audio file is: " + extracted_text)
        except sr.UnknownValueError:
            print("Could not understand the audio")
            await message.answer("Could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            await message.answer("Could not request results")
        finally:
            delete_handled_file.delay(voice_message_path)
            delete_handled_file.delay(voice_message_path_output)
