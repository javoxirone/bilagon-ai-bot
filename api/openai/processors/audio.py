from api.openai.base import OpenAIAPIBase
from exceptions.api import APIServerError


class AudioProcessor(OpenAIAPIBase):
    def __init__(self, api_key: str, base_url: str):
        super().__init__(api_key, base_url)

    def transcribe_audio(self, file: any, model: str = "whisper-1", **kwargs):
        try:
            return self.request(
                endpoint="audio",
                model=model,
                file=file,
                **kwargs
            )
        except APIServerError as e:
            raise APIServerError("Error occurred while transcribing audio.") from e
