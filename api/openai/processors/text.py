from api.openai.base import OpenAIAPIBase
from exceptions.api import APIServerError


class TextProcessor(OpenAIAPIBase):
    def __init__(self, api_key: str, base_url: str):
        super().__init__(api_key, base_url)

    def generate_text_response(self,
                               messages: any,
                               model: str = "gpt-4o-mini",
                               temperature: float = 0.7,
                               max_tokens: int = 16_384,
                               stream: bool = False,
                               stop: None | bool = None,
                               **kwargs):
        try:
            return self.request(
                endpoint="text",
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                stop=stop,
                **kwargs
            )
        except APIServerError as e:
            raise APIServerError("Error occurred while generating chat response.") from e