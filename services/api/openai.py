from config.integrations import text_processor


def get_text_response_in_incognito_mode(user_message: str):
    stream = text_processor.generate_text_response(messages=[{"role": "user", "content": user_message}], stream=True, max_tokens=2000)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None and chunk.choices[0].delta.content != "":
            yield chunk.choices[0].delta.content
