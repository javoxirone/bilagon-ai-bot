from openai import OpenAI


class OpenAIAPIBase:
    def __init__(self, api_key: str, base_url: str):
        self.api_key: str = api_key
        self.base_url: str = base_url
        self.client: OpenAI = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def request(self, endpoint: str, **kwargs):
        if endpoint == "text":
            return self.client.chat.completions.create(**kwargs)
        elif endpoint == "audio":
            return self.client.audio.transcriptions.create(**kwargs)
        elif endpoint == "image":
            pass
        else:
            raise ValueError("Invalid endpoint.")
